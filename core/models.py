from django.db import models
from django.urls import reverse

from core.enums import MonthEnum


class Book(models.Model):
    title = models.CharField(max_length=100)
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
    last_name = models.CharField(max_length=50)
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
    publication_year = models.PositiveSmallIntegerField(null=True, blank=True)
    isbn = models.CharField(
        max_length=20,
        null=True, blank=True,
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
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('publisher_detail', kwargs={'pk': self.pk})


class BookSeries(models.Model):
    name = models.CharField(max_length=100)
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
    )

    def __str__(self):
        return self.period

    def get_absolute_url(self):
        return self.book_edition.get_absolute_url()

    @property
    def period(self):
        if self.year_start == self.year_finish:
            result = (
                f'{self.get_month_start_display()} - '
                f'{self.get_month_finish_display()} '
                f'{self.year_start}'
            )
        else:
            result = (
                f'{self.get_month_start_display()} {self.year_start} - '
                f'{self.get_month_finish_display()} {self.year_finish}'
            )

        return result

    # @property
    # def period(self):
    #     if self.year_start == self.year_finish:
    #         if (
    #             self.month_start == MonthEnum.March and
    #             self.month_finish == MonthEnum.May
    #         ):
    #             result = f'Spring {self.year_start}'
    #         elif (
    #             self.month_start == MonthEnum.June and
    #             self.month_finish == MonthEnum.August
    #         ):
    #             result = f'Summer {self.year_start}'
    #         elif (
    #             self.month_start == MonthEnum.September and
    #             self.month_finish == MonthEnum.November
    #         ):
    #             result = f'Autumn {self.year_start}'
    #         elif self.month_start:
    #             result = f'{self.get_month_start_display()} {self.year_start}'
    #         else:
    #             result = str(self.year_start)
    #     elif not self.year_start:
    #         if self.month_finish:
    #             result = f'{self.get_month_finish_display()} {self.year_finish}'
    #         else:
    #             result = str(self.year_finish)
    #     elif not self.year_finish:
    #         if self.month_start:
    #             result = f'{self.get_month_start_display()} {self.year_start}'
    #         else:
    #             result = str(self.year_start)
    #     else:
    #         if (
    #             self.year_finish.year - self.year_start.year == 1 and
    #             self.month_start == MonthEnum.December and
    #             self.month_finish == MonthEnum.February
    #         ):
    #             result = f'Winter {self.year_start} - {self.year_finish}'
    #         else:
    #             if self.month_start:
    #                 result_1 = f'{self.month_start} {self.year_start}'
    #             else:
    #                 result_1 = self.year_start
    #
    #             if self.month_finish:
    #                 result_2 = f'{self.month_finish} {self.year_finish}'
    #             else:
    #                 result_2 = self.year_finish
    #
    #             result = f'{result_1} - {result_2}'
    #
    #     return result

    @property
    def period_for_template(self):
        if self.year_start == self.year_finish:
            year_start_link = (
                f'<a href="{self.year_start.get_absolute_url()}">'
                f'{self.year_start}'
                f'</a>'
            )
            result = (
                f'{self.get_month_start_display()} - '
                f'{self.get_month_finish_display()} '
                f'{year_start_link}'
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
            result = (
                f'{self.get_month_start_display()} {year_start_link} - '
                f'{self.get_month_finish_display()} {year_finish_link}'
            )

        return result

    # @property
    # def period_for_template(self):
    #     if self.year_start == self.year_finish:
    #         year_start_link = (
    #             f'<a href="{self.year_start.get_absolute_url()}">'
    #             f'{self.year_start}'
    #             f'</a>'
    #         )
    #         if (
    #             self.month_start == MonthEnum.March and
    #             self.month_finish == MonthEnum.May
    #         ):
    #             result = f'Spring {year_start_link}'
    #         elif (
    #             self.month_start == MonthEnum.June and
    #             self.month_finish == MonthEnum.August
    #         ):
    #             result = f'Summer {year_start_link}'
    #         elif (
    #             self.month_start == MonthEnum.September and
    #             self.month_finish == MonthEnum.November
    #         ):
    #             result = f'Autumn {year_start_link}'
    #         elif self.month_start:
    #             result = f'{self.get_month_start_display()} {year_start_link}'
    #         else:
    #             result = year_start_link
    #     elif not self.year_start:
    #         year_finish_link = (
    #             f'<a href="{self.year_finish.get_absolute_url()}">'
    #             f'{self.year_finish}'
    #             f'</a>'
    #         )
    #         if self.month_finish:
    #             result = f'{self.get_month_finish_display()} {year_finish_link}'
    #         else:
    #             result = year_finish_link
    #     elif not self.year_finish:
    #         year_start_link = (
    #             f'<a href="{self.year_start.get_absolute_url()}">'
    #             f'{self.year_start}'
    #             f'</a>'
    #         )
    #         if self.month_start:
    #             result = f'{self.get_month_start_display()} {year_start_link}'
    #         else:
    #             result = year_start_link
    #     else:
    #         year_start_link = (
    #             f'<a href="{self.year_start.get_absolute_url()}">'
    #             f'{self.year_start}'
    #             f'</a>'
    #         )
    #         year_finish_link = (
    #             f'<a href="{self.year_finish.get_absolute_url()}">'
    #             f'{self.year_finish}'
    #             f'</a>'
    #         )
    #         if (
    #             self.year_finish.year - self.year_start.year == 1 and
    #             self.month_start == MonthEnum.December and
    #             self.month_finish == MonthEnum.February
    #         ):
    #             result = f'Winter {year_start_link} - {year_finish_link}'
    #         else:
    #             if self.month_start:
    #                 result_1 = f'{self.get_month_start_display()} {year_start_link}'
    #             else:
    #                 result_1 = year_start_link
    #
    #             if self.month_finish:
    #                 result_2 = f'{self.get_month_finish_display()} {year_finish_link}'
    #             else:
    #                 result_2 = year_finish_link
    #
    #             result = f'{result_1} - {result_2}'
    #
    #     return result
