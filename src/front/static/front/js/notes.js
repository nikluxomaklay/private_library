/**
 * Notes JavaScript - Dynamic inline formset behavior
 * Compatible with django-autocomplete-light
 */

(function() {
    'use strict';

    // Wait for jQuery to be available
    function waitForjQuery(callback) {
        if (typeof jQuery !== 'undefined') {
            callback(jQuery);
        } else {
            setTimeout(function() {
                waitForjQuery(callback);
            }, 50);
        }
    }

    waitForjQuery(function($) {
        $(document).ready(function() {
            var formsetContainer = $('#formset-container');
            var addFormButton = $('#add-form');
            
            // Use the correct prefix from Django formset (book_editions)
            var totalFormsInput = $('#id_book_editions-TOTAL_FORMS');
            
            if (!addFormButton.length || !formsetContainer.length || !totalFormsInput.length) {
                return;
            }
            
            // Store the first form as a template (for cloning new forms)
            var $templateForm = formsetContainer.find('.formset-item').first().clone();
            
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
            
            // Initialize existing forms - setup additional_info behavior
            formsetContainer.find('[name*="book_edition"]').each(function() {
                var $select = $(this);
                setupAdditionalInfoBehavior($select);
            });
            
            // Add new form button click handler
            addFormButton.on('click', function(e) {
                e.preventDefault();
                
                var totalForms = parseInt(totalFormsInput.val(), 10);
                var newFormIndex = totalForms;
                
                // Clone from template
                var $newForm = $templateForm.clone();
                
                // Update indices in cloned form - use book_editions prefix
                $newForm.find(':input').each(function() {
                    var $this = $(this);
                    ['name', 'id'].forEach(function(attr) {
                        var oldVal = $this.attr(attr);
                        if (oldVal) {
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
                }
                
                // Add delete button for new form
                var $actionsDiv = $newForm.find('.mt-2');
                if ($actionsDiv.length) {
                    $actionsDiv.html('<button type="button" class="btn btn-outline-danger btn-sm remove-form">Удалить</button>');
                }
                
                // Append form to container
                formsetContainer.append($newForm);
                
                // Update TOTAL_FORMS
                totalFormsInput.val(totalForms + 1);
                
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
                    
                    // Trigger DAL's initialization for the new element
                    if ($.fn.autocomplete) {
                        $newSelect.autocomplete({
                            url: $newSelect.data('autocomplete-url') || '/book-edition/autocomplete/',
                            theme: $newSelect.data('theme') || 'bootstrap-5'
                        });
                    }
                    
                    // Setup additional_info behavior
                    setupAdditionalInfoBehavior($newSelect);
                }
            });
            
            // Delete form button click handler (event delegation)
            formsetContainer.on('click', '.remove-form', function(e) {
                e.preventDefault();
                
                var $formItem = $(this).closest('.formset-item');
                if (!$formItem.length) {
                    return;
                }
                
                // Check if form has instance.pk (hidden id field with value)
                var $hiddenIdInput = $formItem.find('.hidden input');
                var hasInstancePk = $hiddenIdInput.length && $hiddenIdInput.val();
                
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
                            }
                        }
                        if ($deleteCheckbox.length) {
                            $deleteCheckbox.prop('checked', true);
                        }
                        $actionsDiv.html('<span class="text-danger"><i class="bi bi-trash"></i> Помечено на удаление</span>');
                    }
                } else {
                    // New form: remove from DOM
                    $formItem.remove();
                }
            });
        });
    });
})();
