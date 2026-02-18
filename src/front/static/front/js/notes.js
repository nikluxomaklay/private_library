/**
 * Notes JavaScript - Dynamic inline formset behavior
 * Compatible with django-autocomplete-light
 */

console.log('notes.js: File loaded');

// Wait for jQuery and DOM to be ready
function initNotes() {
    console.log('notes.js: initNotes called');
    
    if (typeof window.jQuery === 'undefined') {
        console.log('notes.js: jQuery not available, waiting...');
        setTimeout(initNotes, 100);
        return;
    }
    
    var $ = window.jQuery;
    console.log('notes.js: jQuery version', $.fn.jquery);
    
    $(document).ready(function() {
        console.log('notes.js: document ready');
        
        var formsetContainer = $('#formset-container');
        var addFormButton = $('#add-form');
        
        // Use the correct prefix from Django formset (book_editions)
        var totalFormsInput = $('#id_book_editions-TOTAL_FORMS');
        
        console.log('notes.js: Elements found', {
            formsetContainer: formsetContainer.length,
            addFormButton: addFormButton.length,
            totalFormsInput: totalFormsInput.length,
            totalFormsInputId: totalFormsInput.attr('id')
        });
        
        if (!addFormButton.length || !formsetContainer.length || !totalFormsInput.length) {
            console.log('notes.js: Missing required elements');
            return;
        }
        
        // Store the first form as a template (for cloning new forms)
        // Don't clone events - we'll initialize them fresh
        var $templateForm = formsetContainer.find('.formset-item').first().clone();
        console.log('notes.js: Template form stored');
        
        // Function to update additional_info behavior
        function setupAdditionalInfoBehavior($select) {
            var formItem = $select.closest('.formset-item');
            if (!formItem.length) return;
            
            var $additionalInfo = formItem.find('[name*="additional_info"]');
            if (!$additionalInfo.length) return;
            
            // Initialize: disable if book_edition not selected
            if (!$select.val()) {
                $additionalInfo.prop('disabled', true).val('');
            }
            
            // Change handler
            $select.on('change', function() {
                if ($(this).val()) {
                    $additionalInfo.prop('disabled', false);
                } else {
                    $additionalInfo.prop('disabled', true).val('');
                }
            });
        }
        
        // Initialize existing forms - DAL already initialized select2, just setup additional_info
        formsetContainer.find('[name*="book_edition"]').each(function() {
            var $select = $(this);
            console.log('notes.js: Setting up additional_info for existing select:', this.name);
            setupAdditionalInfoBehavior($select);
        });
        
        // Add new form button click handler
        addFormButton.on('click', function(e) {
            e.preventDefault();
            console.log('notes.js: Add form button clicked');
            
            var totalForms = parseInt(totalFormsInput.val(), 10);
            var newFormIndex = totalForms;
            
            console.log('notes.js: Current total forms:', totalForms, 'New index:', newFormIndex);
            
            // Clone from template
            var $newForm = $templateForm.clone();
            
            console.log('notes.js: Cloning from template');
            
            // Update indices in cloned form - use book_editions prefix
            $newForm.find(':input').each(function() {
                var $this = $(this);
                ['name', 'id'].forEach(function(attr) {
                    var oldVal = $this.attr(attr);
                    if (oldVal) {
                        // Replace book_editions-N- or book_editions-__prefix__- with new index
                        var newVal = oldVal.replace(/book_editions-(__prefix__|\d+)-/, 'book_editions-' + newFormIndex + '-');
                        $this.attr(attr, newVal);
                    }
                });
            });
            
            // Clear field values (except hidden fields)
            $newForm.find('input:not([type="hidden"]), select, textarea').each(function() {
                var $this = $(this);
                if ($this.is(':checkbox') || $this.is(':radio')) {
                    $this.prop('checked', false);
                } else if (!$this.is('select')) {
                    $this.val('');
                }
            });
            
            // Clear hidden id field (this is a new form without instance.pk)
            var $hiddenIdInput = $newForm.find('.hidden input');
            if ($hiddenIdInput.length) {
                $hiddenIdInput.val('');
                console.log('notes.js: Cleared hidden id field');
            }
            
            // Add delete button for new form
            var $actionsDiv = $newForm.find('.mt-2');
            if ($actionsDiv.length) {
                $actionsDiv.html('<button type="button" class="btn btn-outline-danger btn-sm remove-form">Удалить</button>');
                console.log('notes.js: Added delete button');
            }
            
            // Append form to container
            formsetContainer.append($newForm);
            console.log('notes.js: Appended new form');
            
            // Update TOTAL_FORMS
            totalFormsInput.val(totalForms + 1);
            console.log('notes.js: Updated TOTAL_FORMS to', totalForms + 1);
            
            // Initialize the new form's book_edition select
            var $newSelect = $newForm.find('[name*="book_edition"]');
            if ($newSelect.length) {
                // Get the original select to copy data attributes
                var $originalSelect = formsetContainer.find('.formset-item').first().find('[name*="book_edition"]').first();
                
                // Copy data attributes from original select
                ['autocomplete-url', 'placeholder', 'allow-clear', 'theme'].forEach(function(attr) {
                    var val = $originalSelect.data(attr);
                    if (val !== undefined) {
                        $newSelect.data(attr, val);
                    }
                });
                
                console.log('notes.js: Copied data attributes from original select');
                
                // Trigger DAL's initialization for the new element
                // DAL listens for this event and initializes autocomplete
                if ($.fn.autocomplete) {
                    $newSelect.autocomplete({
                        url: $newSelect.data('autocomplete-url') || '/book-edition/autocomplete/',
                        theme: $newSelect.data('theme') || 'bootstrap-5'
                    });
                    console.log('notes.js: Triggered DAL autocomplete initialization');
                }
                
                // Setup additional_info behavior
                setupAdditionalInfoBehavior($newSelect);
                console.log('notes.js: Initialized additional_info for new form');
            }
        });
        
        // Delete form button click handler (event delegation)
        formsetContainer.on('click', '.remove-form', function(e) {
            e.preventDefault();
            console.log('notes.js: Delete button clicked');
            
            var $formItem = $(this).closest('.formset-item');
            if (!$formItem.length) {
                console.log('notes.js: No form item found');
                return;
            }
            
            // Check if form has instance.pk (hidden id field with value)
            var $hiddenIdInput = $formItem.find('.hidden input');
            var hasInstancePk = $hiddenIdInput.length && $hiddenIdInput.val();
            
            console.log('notes.js: Has instance PK:', hasInstancePk);
            
            if (hasInstancePk) {
                // Existing form: show DELETE checkbox instead of removing from DOM
                var $actionsDiv = $formItem.find('.mt-2');
                if ($actionsDiv.length) {
                    // Find or create DELETE field
                    var $deleteCheckbox = $formItem.find('input[id$="-DELETE"]');
                    if (!$deleteCheckbox.length) {
                        // Create DELETE field
                        var bookEditionName = $formItem.find('[name*="book_edition"]').attr('name');
                        if (bookEditionName) {
                            var deleteName = bookEditionName.replace('book_edition', 'DELETE');
                            $deleteCheckbox = $('<input type="checkbox" hidden>').attr('name', deleteName);
                            $formItem.append($deleteCheckbox);
                            console.log('notes.js: Created DELETE field with name:', deleteName);
                        }
                    }
                    if ($deleteCheckbox.length) {
                        $deleteCheckbox.prop('checked', true);
                        console.log('notes.js: Marked form for deletion');
                    }
                    $actionsDiv.html('<span class="text-danger"><i class="bi bi-trash"></i> Помечено на удаление</span>');
                }
            } else {
                // New form: remove from DOM
                $formItem.remove();
                console.log('notes.js: Removed new form from DOM');
                // Note: Don't decrement TOTAL_FORMS, Django handles deleted forms
            }
        });
        
        console.log('notes.js: Initialization complete');
    });
}

// Start initialization
initNotes();
