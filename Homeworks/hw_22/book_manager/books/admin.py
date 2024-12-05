from django.contrib import admin
from django import forms
from .models import Author, Book, Review


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Author instances.

    Features:
    - Displays name and date of birth in the list view.
    - Provides a search field to find authors by name.
    """
    list_display = ('name', 'date_of_birth')
    search_fields = ('name',)


class BookForm(forms.ModelForm):
    """
    Custom form for the Book model.

    Features:
    - Displays authors as a checkbox select multiple field.
    """
    class Meta:
        model = Book
        fields = '__all__'
        widgets = {
            'authors': forms.CheckboxSelectMultiple(),
        }


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Book instances.

    Features:
    - Uses a custom form to enhance author selection.
    - Displays title, authors, and publication date in the list view.
    - Enables searching by title and filtering by authors.
    - Displays authors in a comma-separated list in the list view.
    """
    form = BookForm
    list_display = ('title', 'display_authors', 'publication_date')
    search_fields = ('title',)
    list_filter = ('authors',)
    filter_horizontal = ('authors',)

    def display_authors(self, obj):
        """
        Return a comma-separated string of author names for a book.

        :param obj: The Book instance.
        :return: Comma-separated author names.
        """
        return ', '.join([author.name for author in obj.authors.all()])
    display_authors.short_description = 'Authors'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Review instances.

    Features:
    - Displays book, reviewer name, rating, and creation date in the list view.
    - Allows filtering by rating and creation date.
    - Enables searching by reviewer name and comment.
    """
    list_display = ('book', 'reviewer_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reviewer_name', 'comment')
