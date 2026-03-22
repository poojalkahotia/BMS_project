// Global Keydown Handler for "Enter as Tab" functionality
document.addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        const target = event.target;
        
        // Exclude Links and Buttons from triggering navigation (allow default click behavior)
        if (target.tagName === 'A' || target.tagName === 'BUTTON') {
            return; 
        }

        // Prevent default behavior (e.g., Form Submission, New Line in Textarea)
        event.preventDefault();

        // Get all potential focusable elements in DOM order
        const form = target.closest('form');
        let allElements;

        if (form) {
            allElements = Array.from(form.querySelectorAll('input, select, textarea, button'));
        } else {
            allElements = Array.from(document.querySelectorAll('input, select, textarea, button'));
        }

        // Find current element's index
        const currentIndex = allElements.indexOf(target);

        // helper to check if element is a valid focus target
        function isValidTarget(el) {
            return colsestVisible(el) && !el.disabled && !el.hasAttribute('readonly') && el.tabIndex >= 0;
        }
        
        // Helper to check visibility
        function colsestVisible(el) {
            return el.offsetParent !== null; 
        }

        // Search forward for the next valid target
        if (currentIndex > -1) {
            for (let i = currentIndex + 1; i < allElements.length; i++) {
                const nextEl = allElements[i];
                if (isValidTarget(nextEl)) {
                    nextEl.focus();
                    break;
                }
            }
        }
    }
});
