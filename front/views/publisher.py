from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from dal import autocomplete

from core.models import Publisher


class PublisherListView(ListView):
    template_name = 'publisher/publisher_list.html'
    model = Publisher
    ordering = 'name'


class PublisherNewView(CreateView):
    template_name = 'publisher/publisher_new.html'
    model = Publisher
    fields = (
        'name',
    )


class PublisherDetailView(DetailView):
    template_name = 'publisher/publisher_detail.html'
    model = Publisher
    fields = (
        'name',
    )


class PublisherUpdateView(UpdateView):
    template_name = 'publisher/publisher_update.html'
    model = Publisher
    fields = (
        'name',
    )


class PublisherDeleteView(DeleteView):
    model = Publisher
    template_name = 'publisher/publisher_delete.html'
    success_url = reverse_lazy('publisher')
    fields = ()


class PublisherAutocompleteView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Publisher.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
