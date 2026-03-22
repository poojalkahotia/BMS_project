/* 
 * ERP-Style Enter Key Navigation
 * - Moves focus to the next field on Enter
 * - Skips hidden/disabled fields
 * - Selects text on focus (optional, good for data entry)
 * - Allows default execution for Buttons and Textareas
 */

document.addEventListener('keydown', function (event) {
    if (event.key !== 'Enter') return;

    const target = event.target;
    
    // 1. Check if it's a form element
    const allowedTags = ['INPUT', 'SELECT', 'TEXTAREA', 'BUTTON'];
    if (!allowedTags.includes(target.tagName)) return;

    // 2. Handle Textareas (Shift+Enter for new line)
    if (target.tagName === 'TEXTAREA' && !event.shiftKey) {
        event.preventDefault(); // Default behavior is new line, we want to move next unless Shift is pressed
        // Fall through to navigation logic
    }
    
    // 3. Handle Buttons
    if (target.tagName === 'BUTTON') {
        // If it's a submit button or has specific action, let it execute 'click'
        // If it has 'data-next', we might want to navigate AFTER click.
        // For now, let's assume buttons are "action points". 
        // If the user wants to navigate FROM a button, they can use data-next.
        if (target.getAttribute('data-next')) {
            event.preventDefault();
            target.click(); // Execute action
            const nextId = target.getAttribute('data-next');
            const nextEl = document.getElementById(nextId);
            if (nextEl) setTimeout(() => nextEl.focus(), 100); // Tiny delay to ensure click finishes
            return;
        }
        // Otherwise, let default Enter on button work (click)
        return; 
    }

    // 4. Prevent default Entry behavior (except for buttons handled above)
    event.preventDefault();

    // 5. Find the form
    const form = target.form;
    if (!form) return;

    // 6. Build the focusable list
    const elements = Array.from(form.elements).filter(el => {
        return allowedTags.includes(el.tagName) &&
            !el.disabled &&
            !el.hidden &&
            !el.readOnly && // CRITICAL: Skip readonly fields
            (el.offsetParent !== null) && 
            el.tabIndex !== -1;
    });

    // 7. Find next element
    const index = elements.indexOf(target);
    if (index > -1 && index < elements.length - 1) {
        let nextElement = elements[index + 1];
        
        // Custom Override: Check if current element has 'data-next' override
        if (target.getAttribute('data-next')) {
            const nextId = target.getAttribute('data-next');
            const overrideEl = document.getElementById(nextId);
            if (overrideEl) nextElement = overrideEl;
        }

        nextElement.focus();
        if (nextElement.tagName === 'INPUT' && !['checkbox', 'radio', 'button', 'submit'].includes(nextElement.type)) {
            nextElement.select(); // Highlight text for easy replacement
        }
    } else {
        // End of form or last element
        // Maybe loop back to save button?
    }
});
