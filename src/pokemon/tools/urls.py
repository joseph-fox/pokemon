import os


def get_vendor_id_from_url(url: str) -> str:
    url_with_no_trailing_slash = url.rstrip('/')
    return url_with_no_trailing_slash.split(os.sep)[-1]
