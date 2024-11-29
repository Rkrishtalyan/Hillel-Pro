from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'count_posts')

    def count_posts(self, obj):
        return obj.post_set.count()
    count_posts.short_description = 'Number of Posts'


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class CommentInline(admin.TabularInline):
    model = models.Comment
    extra = 1
    fields = ('user', 'message', 'created_at')
    readonly_fields = ('user', 'created_at',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_description', 'created_at', 'user', 'is_active', 'view_comments_link')
    list_filter = ('created_at', 'is_active')
    search_fields = ('title', 'body')
    filter_horizontal = ('tag',)
    inlines = [CommentInline]

    def view_comments_link(self, obj):
        count = obj.comments.count()
        url = reverse('admin:blog_comment_changelist') + f'?post__id__exact={obj.id}'
        return format_html('<a href="{}">{} Comment(s)</a>', url, count)

    view_comments_link.short_description = 'Comments'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'user', 'short_description', 'created_at')

admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
