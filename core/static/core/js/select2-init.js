/**
 * Global Select2 Initialization Script
 * Automatically binds Select2 to all elements with the .select2 class
 */

$(document).ready(function() {
    // Initialize standard Select2
    $('.select2').select2({
        theme: 'bootstrap-5',
        width: '100%',
        placeholder: 'Search or select...',
        allowClear: true,
        // Optional keyboard fix for nested modals
        dropdownParent: $('body')
    });
    
    // Auto-focus on search box when dropdown opens
    $(document).on('select2:open', () => {
        setTimeout(() => {
            document.querySelector('.select2-search__field').focus();
        }, 50);
    });
});
