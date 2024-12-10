"""
Admin configuration for the web_site app.

This module customizes the Django admin interface for managing the Article,
Comment, SiteMetric, and Contact models.
"""

from django.contrib import admin

from web_site.models import Article, Comment, SiteMetric, Contact


class CommentInline(admin.TabularInline):
    """
    Inline admin configuration for adding comments directly in the Article admin.
    """
    model = Comment
    extra = 1


def mark_as_reviewed(modeladmin, request, queryset):
    """
    Mark selected articles as reviewed.

    This action updates the 'reviewed' field of selected articles to True.

    :param modeladmin: The admin instance handling the action.
    :type modeladmin: ModelAdmin
    :param request: The HTTP request instance.
    :type request: HttpRequest
    :param queryset: The queryset of selected articles.
    :type queryset: QuerySet
    """
    queryset.update(reviewed=True)

mark_as_reviewed.short_description = "Mark selected articles as reviewed"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Article model.

    - Displays title, category, reviewed status, and associated contact.
    - Allows filtering by category and reviewed status.
    - Includes a custom action to mark articles as reviewed.
    - Supports adding comments inline.
    """
    list_display = ('title', 'category', 'reviewed', 'contact')
    list_filter = ('category', 'reviewed')
    actions = [mark_as_reviewed]
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.

    - Displays article, text, and creation date of the comment.
    - Allows filtering by article and creation date.
    """
    list_display = ('article', 'text', 'created_at')
    list_filter = ('article', 'created_at')


# Task 9

@admin.register(SiteMetric)
class SiteMetricAdmin(admin.ModelAdmin):
    """
    Admin configuration for the SiteMetric model.

    - Displays the request count field.
    """
    list_display = ('request_count',)


# Task 10

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contact model.

    - Displays name and phone fields.
    """
    list_display = ('name', 'phone')
