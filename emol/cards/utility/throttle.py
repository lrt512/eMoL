"""Throttle tools for emol"""

from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect


def throttle(limit, window, key=None):
    """
    Decorator for throttling the rate of requests for a given view function.
    :param rate: the maximum number of requests allowed within the duration
    :param duration: the duration of the throttling window in seconds
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)

            ip_address = request.META.get("REMOTE_ADDR")
            if key is None:
                cache_key = f"throttle:{ip_address}"
            else:
                cache_key = f"throttle:{key}:{ip_address}"

            request_count = cache.get(cache_key, 0)
            if request_count >= limit:
                return redirect("too_many_requests")

            cache.set(cache_key, request_count + 1, window)
            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator
