from django.core.cache import cache 
from rest_framework.throttling import BaseThrottle, UserRateThrottle, AnonRateThrottle

class CreateArticleUserThrottle(UserRateThrottle):
    scope = 'create_article_user'

class CreateArticleAnonThrottle(AnonRateThrottle):
    scope = 'create_article_anon'

class ListArticlesUserThrottle(UserRateThrottle):
    scope = 'list_articles_user'

class ListArticlesAnonThrottle(AnonRateThrottle):
    scope = 'list_articles_anon'


class BlogRateThrottle(BaseThrottle):
    def allow_request(self, request, view):
        if request.user.is_authenticated:
            user_id = f'user_{request.user.id}'
            max_requests = 5
            print(user_id)
        else:
            user_id = f"anon_{request.Meta.get('REMOTE_ADDR')}"
            max_requests = 1
            print(user_id)

        path = request.path
        cache_key = f"throttle_{user_id}_{path}"
        hit_count = cache.get(cache_key, 0)

        if hit_count > max_requests:
            return False
        else:
            cache.set(cache_key, hit_count + 1, timeout=30)
            return True