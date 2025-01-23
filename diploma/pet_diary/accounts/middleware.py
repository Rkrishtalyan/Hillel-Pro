from django.utils import translation, timezone
from django.utils.deprecation import MiddlewareMixin
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class UserLocaleTimeZoneMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        if user.is_authenticated:
            lang = user.preferred_language or 'ua'
            translation.activate(lang)
            request.LANGUAGE_CODE = lang

            timezone_str = user.preferred_timezone or 'UTC'
        else:
            lang = request.session.get('language', 'ua')
            translation.activate(lang)
            request.LANGUAGE_CODE = lang

            timezone_str = request.session.get('timezone', 'UTC')

        try:
            user_tz = ZoneInfo(timezone_str)
        except ZoneInfoNotFoundError:
            user_tz = ZoneInfo('UTC')
        except Exception:
            user_tz = ZoneInfo('UTC')

        timezone.activate(user_tz)

    def process_response(self, request, response):
        translation.deactivate()
        timezone.deactivate()
        return response
