from .settings import *  # noqa

DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0", "localhost"]

CELERY_TASK_ALWAYS_EAGER = True

# Dump logs to console
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "{levelname} {message}", "style": "{"}
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"}
    },
    "loggers": {"": {"handlers": ["console"], "level": "INFO"}},
}

SITE_DOMAIN = "0.0.0.0:8090"
