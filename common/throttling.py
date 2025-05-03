from rest_framework.throttling import UserRateThrottle
from rest_framework.throttling import ScopedRateThrottle


class PremiumUserRateThrottle(UserRateThrottle):
    scope = 'premium'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated and request.user.profile.is_premium:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }


class RoleBasedScopedRateThrottle(ScopedRateThrottle):
    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            self.scope = getattr(view, 'throttle_scope_general', self.scope)
        elif getattr(request.user, 'is_premium', False):
            self.scope = getattr(view, 'throttle_scope_premium', self.scope)
        else:
            self.scope = getattr(view, 'throttle_scope_general', self.scope)

        return super().get_cache_key(request, view)
