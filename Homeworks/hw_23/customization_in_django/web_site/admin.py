from django.contrib import admin
from .models import Article, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1


def mark_as_reviewed(modeladmin, request, queryset):
    queryset.update(reviewed=True)

mark_as_reviewed.short_description = "Mark selected articles as reviewed"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'reviewed')
    list_filter = ('category', 'reviewed')
    actions = [mark_as_reviewed]
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'text', 'created_at')
    list_filter = ('article', 'created_at')
