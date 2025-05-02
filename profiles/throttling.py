from rest_framework.throttling import UserRateThrottle


class PremiumUserThrottle(UserRateThrottle):
    scope = 'premium'

    def allow_request(self, request, view):
        user = request.user
        if user.is_authenticated and getattr(user, 'is_premium', False):
            return super().allow_request(request, view)
        return True
