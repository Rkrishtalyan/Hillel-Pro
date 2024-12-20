"""
Module for background tasks in the board app.

This module defines background tasks that are scheduled to run asynchronously
to handle specific actions related to the `Ad` model. The tasks are implemented
using the `background_task` library, enabling deferred execution of operations.

Functions:
    - deactivate_ad_task: Deactivates an `Ad` instance after a set period.
"""

# ---- Imports ----
from background_task import background

from .models import Ad


# ---- Background Tasks ----

@background(schedule=30 * 24 * 60 * 60)
def deactivate_ad_task(ad_id):
    """
    Deactivate an Ad instance after a scheduled time.

    :param ad_id: The ID of the Ad to deactivate.
    :type ad_id: int
    """
    try:
        ad = Ad.objects.get(pk=ad_id)
        if ad.is_active:
            ad.is_active = False
            ad.save()
    except Ad.DoesNotExist:
        pass
