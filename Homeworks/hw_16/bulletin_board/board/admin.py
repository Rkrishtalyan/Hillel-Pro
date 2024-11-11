# ---- Imports ----
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from . import models

# ---- Admin classes ----

class UserAdmin(admin.ModelAdmin):
    """Admin view for User with list display configuration."""
    list_display = ('id', 'username', 'first_name', 'last_name', 'phone_number', 'address')


class CategoryAdmin(admin.ModelAdmin):
    """Admin view for Category with list display and active ad count."""
    list_display = ('id', 'name', 'description', 'count_active_ads')


class CommentInline(admin.TabularInline):
    """Inline admin view for Comments related to Ads."""
    model = models.Comment
    extra = 1
    fields = ('user', 'content', 'created_at')
    readonly_fields = ('user', 'created_at',)


class AdAdmin(admin.ModelAdmin):
    """Admin view for Ads with list display, filtering, and comment view link."""
    list_display = ('id', 'title', 'short_description', 'created_at', 'user', 'view_comments_link')
    list_filter = ('category', 'is_active', 'price', 'created_at')
    search_fields = ('title', 'description')
    filter_horizontal = ('category',)
    inlines = [CommentInline]

    def view_comments_link(self, obj):
        """
        Return a link to view comments for a specific Ad instance.

        :param obj: The Ad instance.
        :type obj: models.Ad
        :return: HTML link with the number of comments for the Ad.
        :rtype: str
        """
        count = models.Comment.comments_in_ad(obj)
        url = reverse('admin:board_comment_changelist') + '?ad__id__exact=' + str(obj.id)
        return format_html('<a href="{}">{} Comment(s)</a>', url, count)

    view_comments_link.short_description = 'Comments'


class CommentAdmin(admin.ModelAdmin):
    """Admin view for Comments with list display."""
    list_display = ('id', 'ad', 'user', 'short_description',)


# ---- Model Registration ----
admin.site.register(models.UserProfile, UserAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Ad, AdAdmin)
admin.site.register(models.Comment, CommentAdmin)
