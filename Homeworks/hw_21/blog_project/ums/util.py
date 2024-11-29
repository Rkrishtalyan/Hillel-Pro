from ums.models import UserProfile
from django.contrib.auth.models import User

for user in User.objects.all():
    if not hasattr(user, 'userprofile'):
        UserProfile.objects.create(user=user)
