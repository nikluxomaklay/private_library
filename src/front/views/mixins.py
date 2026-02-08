from django.views.generic.list import ListView

class PaginationPageSizeMixin:
    """
    Миксин для поддержки динамического размера страницы через параметр page_size.
    """
    PAGE_SIZE_CHOICES = [10, 25, 50, 100]
    DEFAULT_PAGE_SIZE = 25

    def get_paginate_by(self, queryset):
        try:
            page_size = int(self.request.GET.get('page_size', self.DEFAULT_PAGE_SIZE))
            if page_size not in self.PAGE_SIZE_CHOICES:
                page_size = self.DEFAULT_PAGE_SIZE
        except (TypeError, ValueError):
            page_size = self.DEFAULT_PAGE_SIZE
        return page_size

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_size_choices'] = self.PAGE_SIZE_CHOICES
        try:
            page_size_selected = int(self.request.GET.get('page_size', self.DEFAULT_PAGE_SIZE))
            if page_size_selected not in self.PAGE_SIZE_CHOICES:
                page_size_selected = self.DEFAULT_PAGE_SIZE
        except (TypeError, ValueError):
            page_size_selected = self.DEFAULT_PAGE_SIZE
        context['page_size_selected'] = page_size_selected
        return context 