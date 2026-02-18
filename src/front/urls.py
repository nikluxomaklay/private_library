from django.urls import path

from front.views import author
from front.views import book
from front.views import book_edition
from front.views import book_series
from front.views import index
from front.views import notes
from front.views import publisher
from front.views import reading_log
from front.views import year

urlpatterns = [
    path('', index.IndexPageView.as_view(), name='index'),

    path('author/', author.AuthorListView.as_view(), name='author'),
    path('author/new/', author.AuthorNewView.as_view(), name='author_new'),
    path('author/<int:pk>/', author.AuthorDetailView.as_view(), name='author_detail'),
    path('author/<int:pk>/delete/', author.AuthorDeleteView.as_view(), name='author_delete'),
    path('author/<int:pk>/update/', author.AuthorUpdateView.as_view(), name='author_update'),
    path('author/autocomplete/', author.AuthorAutocompleteView.as_view(), name='author_autocomplete'),

    path('book/', book.BookListView.as_view(), name='book'),
    path('book/new/', book.BookNewView.as_view(), name='book_new'),
    path('book/<int:pk>/', book.BookDetailView.as_view(), name='book_detail'),
    path('book/<int:pk>/delete/', book.BookDeleteView.as_view(), name='book_delete'),
    path('book/<int:pk>/update/', book.BookUpdateView.as_view(), name='book_update'),
    path('book/autocomplete/', book.BookAutocompleteView.as_view(), name='book_autocomplete'),

    path('book-edition/', book_edition.BookEditionListView.as_view(), name='book_edition'),
    path('book-edition/new/', book_edition.BookEditionNewView.as_view(), name='book_edition_new'),
    path('book-edition/<int:pk>/', book_edition.BookEditionDetailView.as_view(), name='book_edition_detail'),
    path('book-edition/<int:pk>/delete/', book_edition.BookEditionDeleteView.as_view(), name='book_edition_delete'),
    path('book-edition/<int:pk>/update/', book_edition.BookEditionUpdateView.as_view(), name='book_edition_update'),
    path('book-edition/autocomplete/', book_edition.BookEditionAutocompleteView.as_view(), name='book_edition_autocomplete'),

    path('book-series/', book_series.BookSeriesListView.as_view(), name='book_series'),
    path('book-series/new/', book_series.BookSeriesNewView.as_view(), name='book_series_new'),
    path('book-series/<int:pk>/', book_series.BookSeriesDetailView.as_view(), name='book_series_detail'),
    path('book-series/<int:pk>/delete/', book_series.BookSeriesDeleteView.as_view(), name='book_series_delete'),
    path('book-series/<int:pk>/update/', book_series.BookSeriesUpdateView.as_view(), name='book_series_update'),
    path('book-series/autocomplete/', book_series.BookSeriesAutocompleteView.as_view(), name='book_series_autocomplete'),

    path('publisher/', publisher.PublisherListView.as_view(), name='publisher'),
    path('publisher/new/', publisher.PublisherNewView.as_view(), name='publisher_new'),
    path('publisher/<int:pk>/', publisher.PublisherDetailView.as_view(), name='publisher_detail'),
    path('publisher/<int:pk>/delete/', publisher.PublisherDeleteView.as_view(), name='publisher_delete'),
    path('publisher/<int:pk>/update/', publisher.PublisherUpdateView.as_view(), name='publisher_update'),
    path('publisher/autocomplete/', publisher.PublisherAutocompleteView.as_view(), name='publisher_autocomplete'),

    path('year/', year.YearListView.as_view(), name='year'),
    path('year/new/', year.YearNewView.as_view(), name='year_new'),
    path('year/<int:pk>/', year.YearDetailView.as_view(), name='year_detail'),
    path('year/<int:pk>/delete/', year.YearDeleteView.as_view(), name='year_delete'),
    path('year/<int:pk>/update/', year.YearUpdateView.as_view(), name='year_update'),

    path('reading-log/new/', reading_log.ReadingLogNewView.as_view(), name='reading_log_new'),
    path('reading-log/', reading_log.ReadingLogListView.as_view(), name='reading_log_list'),

    # Note URLs
    path('note/', notes.NoteListView.as_view(), name='note'),
    path('note/new/', notes.NoteNewView.as_view(), name='note_new'),
    path('note/<int:pk>/', notes.NoteDetailView.as_view(), name='note_detail'),
    path('note/<int:pk>/update/', notes.NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/delete/', notes.NoteDeleteView.as_view(), name='note_delete'),

    # Note autocomplete URLs
    path('note/autocomplete/', notes.NoteAutocompleteView.as_view(), name='note_autocomplete'),
    path('keyword/autocomplete/', notes.KeyWordAutocompleteView.as_view(), name='keyword_autocomplete'),
]
