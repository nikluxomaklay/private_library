/**
 * Notes JavaScript - Dynamic inline formset behavior
 * 
 * Provides:
 * - Dynamic add/remove forms in inline formset
 * - Conditional disabling of additional_info field based on book_edition selection
 */

document.addEventListener('DOMContentLoaded', function() {
    // ==========================================
    // T078: Dynamic inline formset behavior
    // ==========================================
    const formsetContainer = document.getElementById('formset-container');
    const addFormButton = document.getElementById('add-form');
    const totalFormsInput = document.getElementById('id_formset-TOTAL_FORMS');

    if (addFormButton && formsetContainer && totalFormsInput) {
        // Функция для обновления поведения additional_info
        function setupAdditionalInfoBehavior(select) {
            const formItem = select.closest('.formset-item');
            if (!formItem) return;

            const additionalInfo = formItem.querySelector('[name*="additional_info"]');
            if (additionalInfo) {
                // Инициализация: disabled если book_edition не выбран
                if (!select.value) {
                    additionalInfo.disabled = true;
                    additionalInfo.value = '';
                }

                // Обработчик изменения book_edition
                select.addEventListener('change', function() {
                    if (this.value) {
                        additionalInfo.disabled = false;
                    } else {
                        additionalInfo.disabled = true;
                        additionalInfo.value = '';
                    }
                });
            }
        }

        // Инициализируем существующие формы
        document.querySelectorAll('[name*="book_edition"]').forEach(setupAdditionalInfoBehavior);

        // Добавление новой формы
        addFormButton.addEventListener('click', function() {
            const totalForms = parseInt(totalFormsInput.value);
            const newFormIndex = totalForms;

            // Находим шаблон формы (первую форму)
            const firstForm = formsetContainer.querySelector('.formset-item');
            if (!firstForm) return;

            // Клонируем форму
            const newForm = firstForm.cloneNode(true);

            // Обновляем индексы в cloned форме
            newForm.innerHTML = newForm.innerHTML.replace(
                /id_formset-(\d+)-/g,
                'id_formset-' + newFormIndex + '-'
            ).replace(
                /formset-(\d+)-/g,
                'formset-' + newFormIndex + '-'
            );

            // Очищаем значения полей
            newForm.querySelectorAll('input, select, textarea').forEach(function(input) {
                if (input.type === 'checkbox') {
                    input.checked = false;
                } else {
                    input.value = '';
                }
                // Сбрасываем select2 значения если используется jQuery
                if (window.jQuery && input.classList.contains('select2-hidden-accessible')) {
                    window.jQuery(input).val('').trigger('change');
                }
            });

            // Добавляем кнопку удаления
            const actionsDiv = newForm.querySelector('.mt-2');
            if (actionsDiv) {
                actionsDiv.innerHTML = '<button type="button" class="btn btn-outline-danger btn-sm remove-form">Удалить</button>';
            }

            // Добавляем форму в контейнер
            formsetContainer.appendChild(newForm);

            // Обновляем TOTAL_FORMS
            totalFormsInput.value = totalForms + 1;

            // Инициализируем поведение для новой формы
            const newSelect = newForm.querySelector('[name*="book_edition"]');
            if (newSelect) {
                setupAdditionalInfoBehavior(newSelect);
            }

            // Reinitialize select2 для новых элементов если используется jQuery
            if (window.jQuery && typeof window.jQuery.fn.select2 !== 'undefined') {
                window.jQuery(newForm.querySelector('[name*="book_edition"]')).select2({
                    ajax: {
                        url: '/book-edition/autocomplete/',
                        dataType: 'json'
                    }
                });
            }
        });

        // Удаление формы (делегирование событий)
        formsetContainer.addEventListener('click', function(e) {
            if (e.target && e.target.classList.contains('remove-form')) {
                const formItem = e.target.closest('.formset-item');
                if (formItem) {
                    formItem.remove();
                    // Note: TOTAL_FORMS не уменьшаем, Django сам обработает удаленные формы
                }
            }
        });
    }

    // ==========================================
    // T079: Conditional additional_info field disabling
    // ==========================================
    // Эта логика уже включена в setupAdditionalInfoBehavior выше,
    // но добавляем отдельный обработчик для всех select book_edition
    // на случай если они находятся вне formset
    document.querySelectorAll('[name*="book_edition"]').forEach(function(select) {
        // Пропускаем уже обработанные в formset
        if (select.closest('.formset-item')) return;

        select.addEventListener('change', function() {
            const formItem = this.closest('.form-group, .mb-3, div');
            if (!formItem) return;

            const additionalInfo = formItem.querySelector('[name*="additional_info"]');
            if (additionalInfo) {
                if (this.value) {
                    additionalInfo.disabled = false;
                } else {
                    additionalInfo.disabled = true;
                    additionalInfo.value = '';
                }
            }
        });

        // Initial state check
        const event = new Event('change');
        select.dispatchEvent(event);
    });
});
