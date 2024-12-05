from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from .models import Book


# !!!!!!!! Commented to fix MongoDB compatibility issues !!!!!!!!

# ---- Signal Handlers ----
# @receiver(post_save, sender=Book)
# @receiver(post_delete, sender=Book)
# def clear_book_cache(sender, **kwargs):
#     """
#     Clear the cache for the book list whenever a Book instance is saved or deleted.
#
#     This function is triggered by the `post_save` and `post_delete` signals
#     for the `Book` model. It ensures that cached book list data is invalidated
#     when a book is added, updated, or removed.
#
#     :param sender: The model class (Book) that triggered the signal.
#     :param kwargs: Additional arguments passed by the signal.
#     """
#     cache.delete('book_list')
