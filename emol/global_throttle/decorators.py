from functools import wraps

from django.conf import settings


def exempt_from_throttling(view_func):
    """Decorator to exempt a view from global throttling"""

    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.exempt_from_throttling = True
    return wraps(view_func)(wrapped_view)


def testing_throttle_settings(view_func):
    """Temporarily modify throttle settings for testing"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        original_limit = getattr(settings, "GLOBAL_THROTTLE_LIMIT", 10)
        original_window = getattr(settings, "GLOBAL_THROTTLE_WINDOW", 3600)

        # Increase limits during testing
        settings.GLOBAL_THROTTLE_LIMIT = 1000
        settings.GLOBAL_THROTTLE_WINDOW = 3600

        try:
            return view_func(request, *args, **kwargs)
        finally:
            # Restore original settings
            settings.GLOBAL_THROTTLE_LIMIT = original_limit
            settings.GLOBAL_THROTTLE_WINDOW = original_window

    return wrapper
