# ---- Import Statements ----
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

from . import models


# ---- Admin Class Definitions ----

class CategoryAdmin(admin.ModelAdmin):
    """
    Define admin interface for the Category model.

    :var list_display: Fields to display in the admin list view.
    """

    list_display = ('id', 'name', 'description', 'count_posts')

    def count_posts(self, obj):
        """
        Return the count of posts associated with a category.

        :param obj: The category instance.
        :type obj: models.Category
        :return: Number of posts in the category.
        :rtype: int
        """
        return obj.post_set.count()

    count_posts.short_description = 'Number of Posts'


class TagAdmin(admin.ModelAdmin):
    """
    Define admin interface for the Tag model.

    :var list_display: Fields to display in the admin list view.
    """

    list_display = ('id', 'name',)


class CommentInline(admin.TabularInline):
    """
    Define inline admin interface for comments in the Post model.

    :var model: The Comment model to associate inline.
    :var extra: Number of empty forms to display for new comments.
    :var fields: Fields to display in the inline form.
    :var readonly_fields: Fields that are read-only.
    """

    model = models.Comment
    extra = 1
    fields = ('user', 'message', 'created_at')
    readonly_fields = ('user', 'created_at',)


class PostAdmin(admin.ModelAdmin):
    """
    Define admin interface for the Post model.

    :var list_display: Fields to display in the admin list view.
    :var list_filter: Fields to filter by in the admin list view.
    :var search_fields: Fields to include in the search.
    :var filter_horizontal: Many-to-many fields to display with a horizontal widget.
    :var inlines: Inline models to associate with this admin class.
    """

    list_display = (
        'id', 'title', 'short_description', 'created_at',
        'user', 'is_active', 'view_comments_link'
    )
    list_filter = ('created_at', 'is_active')
    search_fields = ('title', 'body')
    filter_horizontal = ('tag',)
    inlines = [CommentInline]

    def view_comments_link(self, obj):
        """
        Generate a link to view comments for a post in the admin interface.

        :param obj: The post instance.
        :type obj: models.Post
        :return: HTML link to the comments admin view.
        :rtype: str
        """
        count = obj.comments.count()
        url = reverse('admin:blog_comment_changelist') + f'?post__id__exact={obj.id}'
        return format_html('<a href="{}">{} Comment(s)</a>', url, count)

    view_comments_link.short_description = 'Comments'


class CommentAdmin(admin.ModelAdmin):
    """
    Define admin interface for the Comment model.

    :var list_display: Fields to display in the admin list view.
    """

    list_display = ('id', 'post', 'user', 'short_description', 'created_at')


# ---- Register Admin Classes ----

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
