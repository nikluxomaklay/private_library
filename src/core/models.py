from django.db import models, transaction
from django.urls import reverse

from core.enums import MonthEnum
from core.helpers import generate_note_number


class Book(models.Model):
    title = models.CharField(max_length=100, db_index=True)  # For filtering
    extended_title = models.CharField(
        max_length=200,
        null=True, blank=True,
    )
    authors = models.ManyToManyField(
        'Author',
        related_name='books',
    )

    title_original = models.CharField(
        max_length=100,
        null=True, blank=True,
    )
    extended_title_original = models.CharField(
        max_length=200,
        null=True, blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book_detail", kwargs={"pk": self.pk})

    def reading_logs(self):
        return ReadingLog.objects.filter(
            book_edition__book=self,
        ).order_by(
            'book_edition__book__title',
        )


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, db_index=True)  # For filtering
    middle_name = models.CharField(
        max_length=50,
        null=True, blank=True,
    )

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("author_detail", kwargs={"pk": self.pk})

    @property
    def full_name(self):
        return ' '.join(
            (
                item for item
                in (
                self.last_name,
                self.first_name,
                self.middle_name,
            )
                if item
            ),
        )

    @property
    def full_name_short(self):
        return ' '.join(
            (
                item for item
                in (
                    self.last_name,
                    self.first_name_short,
                    self.middle_name_short,
                )
                if item
            ),
        )

    @property
    def first_name_short(self):
        if self.first_name:
            return f'{self.first_name[0]}.'
        return None

    @property
    def middle_name_short(self):
        if self.middle_name:
            return f'{self.middle_name[0]}.'
        return None


class BookEdition(models.Model):
    # Define the choices for book edition types
    EDITION_TYPE_CHOICES = [
        ('PAPER_BOOK', 'Paper Book'),
        ('EBOOK', 'E-book'),
        ('AUDIOBOOK', 'Audiobook'),
        ('WEBPAGE', 'Web Page'),
    ]
    
    book = models.ForeignKey(
        'Book',
        on_delete=models.PROTECT,
        related_name='editions',
        null=False, blank=False,
    )
    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.PROTECT,
        related_name='book_editions',
        null=True, blank=True,
    )
    series = models.ForeignKey(
        'BookSeries',
        on_delete=models.PROTECT,
        related_name='book_editions',
        null=True, blank=True,
    )
    publication_year = models.PositiveSmallIntegerField(null=True, blank=True, db_index=True)  # For filtering
    isbn = models.CharField(
        max_length=20,
        null=True, blank=True,
    )
    edition_type = models.CharField(
        max_length=20,
        choices=EDITION_TYPE_CHOICES,
        default='PAPER_BOOK',
        help_text="Type of book edition",
        null=False, blank=False,  # Required field
    )

    def __str__(self):
        return ' - '.join(
            (
                str(item) for item
                in (self.title, self.publisher, self.publication_year)
                if item is not None
            ),
        )

    @property
    def publication_info(self):
        return ' - '.join(
            (
                str(item) for item
                in (self.publisher, self.publication_year)
                if item is not None
            ),
        )

    def get_absolute_url(self):
        return reverse("book_edition_detail", kwargs={"pk": self.pk})

    @property
    def title(self):
        return self.book.title

    @property
    def extended_title(self):
        return self.book.extended_title

    @property
    def title_original(self):
        return self.book.title_original

    @property
    def extended_title_original(self):
        return self.book.extended_title_original

    @property
    def authors(self):
        return self.book.authors


class Publisher(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # For filtering

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('publisher_detail', kwargs={'pk': self.pk})


class BookSeries(models.Model):
    name = models.CharField(max_length=100, db_index=True)  # For filtering
    publisher = models.ForeignKey(
        'Publisher',
        on_delete=models.PROTECT,
        related_name='book_series',
    )

    def __str__(self):
        return f'"{self.name}", {self.publisher}'

    def get_absolute_url(self):
        return reverse('book_series_detail', kwargs={'pk': self.pk})


class Year(models.Model):
    year = models.BigIntegerField(primary_key=True)

    def __str__(self):
        return str(self.year)

    def get_absolute_url(self):
        return reverse('year_detail', kwargs={'pk': self.pk})

    def reading_logs(self):
        return ReadingLog.objects.filter(
            models.Q(year_start=self) | models.Q(year_finish=self),
        )


class ReadingLog(models.Model):
    book_edition = models.ForeignKey(
        'BookEdition',
        on_delete=models.PROTECT,
        related_name='reading_logs',
    )
    year_start = models.ForeignKey(
        'Year',
        on_delete=models.PROTECT,
        related_name='year_start',
        null=True, blank=True,
    )
    month_start = models.IntegerField(
        choices=MonthEnum.choices,
        null=True, blank=True,
        db_index=True  # For filtering
    )
    year_finish = models.ForeignKey(
        'Year',
        on_delete=models.PROTECT,
        related_name='year_finish',
        null=True, blank=True,
    )
    month_finish = models.IntegerField(
        choices=MonthEnum.choices,
        null=True, blank=True,
        db_index=True  # For filtering
    )

    def __str__(self):
        return self.period

    def get_absolute_url(self):
        return self.book_edition.get_absolute_url()

    @property
    def period(self):
        if self.year_start == self.year_finish:
            if not self.month_start or not self.month_finish:
                result = str(self.year_start)
            else:
                result = (
                    f'{self.year_start} '
                    f'{self.get_month_start_display()} - '
                    f'{self.get_month_finish_display()}'
                )
        else:
            if self.month_start:
                start_result = f'{self.year_start} {self.get_month_start_display()}'
            else:
                start_result = str(self.year_start)
            if self.month_finish:
                finish_result = f'{self.year_finish} {self.get_month_finish_display()}'
            else:
                finish_result = str(self.year_finish)

            result = f'{start_result} - {finish_result}'

        return result

    @property
    def period_for_template(self):
        if self.year_start == self.year_finish:
            year_start_link = (
                f'<a href="{self.year_start.get_absolute_url()}">'
                f'{self.year_start}'
                f'</a>'
            )

            if not self.month_start or not self.month_finish:
                result = year_start_link
            else:
                result = (
                    f'{year_start_link} '
                    f'{self.get_month_start_display()} - '
                    f'{self.get_month_finish_display()}'
                )
        else:
            year_start_link = (
                f'<a href="{self.year_start.get_absolute_url()}">'
                f'{self.year_start}'
                f'</a>'
            )
            year_finish_link = (
                f'<a href="{self.year_finish.get_absolute_url()}">'
                f'{self.year_finish}'
                f'</a>'
            )

            if self.month_start:
                start_result = f'{year_start_link} {self.get_month_start_display()}'
            else:
                start_result = year_start_link
            if self.month_finish:
                finish_result = f'{year_finish_link} {self.get_month_finish_display()}'
            else:
                finish_result = year_finish_link

            result = f'{start_result} - {finish_result}'

        return result


class KeyWord(models.Model):
    word = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.word


class Note(models.Model):
    index = models.TextField(db_index=True, unique=True)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
    related_notes = models.ManyToManyField('self')
    keywords = models.ManyToManyField('KeyWord', related_name='notes')
    topic = models.CharField(max_length=255, null=False, blank=False)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.index} {self.topic}'

    def save_base(self, *args, **kwargs):
        if not self.index:
            query = Note.objects.select_for_update().all()
            with transaction.atomic():
                self.index = generate_note_number(self, query)
        super().save_base(*args, **kwargs)


class NoteToBookEdition(models.Model):
    note = models.ForeignKey('Note', on_delete=models.PROTECT, related_name='book_editions')
    book_edition = models.ForeignKey(
        'BookEdition',
        on_delete=models.PROTECT,
        related_name='notes',
    )
    additional_info = models.TextField(null=True, blank=True)
