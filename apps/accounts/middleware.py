from django.contrib.auth.models import User
from django.core.cache import cache
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class ActiveUserMiddleware(MiddlewareMixin):
    '''For checking last online'''
    def process_request(self, request):
        if request.user.is_authenticated and request.session.session_key:
            cache_key = f'last-seen-{request.user.id}'
            last_login = cache.get(cache_key)

            if not last_login:
                User.objects.filter(id=request.user.id).update(last_login=timezone.now())
                # Set caching for 300 seconds with the current date using the last-seen-id-user key
                cache.set(cache_key, timezone.now(), 300)