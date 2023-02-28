from django.utils.crypto import get_random_string


def get_random_32():
    return get_random_string(32)
