# ---- Import Statements ----
from django.contrib import admin
from .models import UserProfile


# ---- Admin Class Definitions ----

class UserProfileAdmin(admin.ModelAdmin):
    """
    Define admin interface for the UserProfile model.

    :var list_display: Fields to display in the admin list view.
    """

    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'bio', 'location')

    def email(self, obj):
        """
        Retrieve the email associated with the user.

        :param obj: The UserProfile instance.
        :type obj: UserProfile
        :return: The user's email address.
        :rtype: str
        """
        return obj.user.email


# ---- Register Admin Classes ----

admin.site.register(UserProfile, UserProfileAdmin)
