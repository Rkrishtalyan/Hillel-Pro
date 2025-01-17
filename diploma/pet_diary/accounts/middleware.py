import pytz
from django.utils import translation, timezone


class UserLocaleTimeZoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            # Lnaguage activation
            lang = user.preferred_language or 'ua'
            translation.activate(lang)
            request.LANGUAGE_CODE = lang

            # Timezone activation
            try:
                user_tz = pytz.timezone(user.preferred_timezone)
            except Exception:
                user_tz = pytz.timezone('UTC')
            timezone.activate(user_tz)

        response = self.get_response(request)

        translation.deactivate()
        timezone.deactivate()

        return response
