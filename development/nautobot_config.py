"""Nautobot development configuration file."""
import os
import sys

from nautobot.core.settings import *  # noqa: F403
from nautobot.core.settings_funcs import is_truthy, parse_redis_connection

BANNER_TOP = "Local"
METRICS_ENABLED = True

#
# Misc. settings
#

ALLOWED_HOSTS = os.getenv("NAUTOBOT_ALLOWED_HOSTS", "").split(" ")
SECRET_KEY = os.getenv("NAUTOBOT_SECRET_KEY", "")

#
# Databases
#

DATABASES = {
    "default": {
        "NAME": os.getenv("NAUTOBOT_DB_NAME", "nautobot"),
        "USER": os.getenv("NAUTOBOT_DB_USER", ""),
        "PASSWORD": os.getenv("NAUTOBOT_DB_PASSWORD", ""),
        "HOST": os.getenv("NAUTOBOT_DB_HOST", "localhost"),
        "PORT": os.getenv("NAUTOBOT_DB_PORT", ""),
        "CONN_MAX_AGE": int(os.getenv("NAUTOBOT_DB_TIMEOUT", 300)),
        "ENGINE": os.getenv("NAUTOBOT_DB_ENGINE", "django.db.backends.postgresql"),
    }
}

# Ensure proper Unicode handling for MySQL
if DATABASES["default"]["ENGINE"] == "django.db.backends.mysql":
    DATABASES["default"]["OPTIONS"] = {"charset": "utf8mb4"}

#
# Debug
#

DEBUG = is_truthy(os.getenv("NAUTOBOT_DEBUG", True))

# Django Debug Toolbar
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda _request: DEBUG and not TESTING}

if "debug_toolbar" not in INSTALLED_APPS:  # noqa: F405
    INSTALLED_APPS.append("debug_toolbar")  # noqa: F405
if "debug_toolbar.middleware.DebugToolbarMiddleware" not in MIDDLEWARE:  # noqa: F405
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405

#
# Logging
#

LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

TESTING = len(sys.argv) > 1 and sys.argv[1] == "test"

# Verbose logging during normal development operation, but quiet logging during unit test execution
if not TESTING:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "normal": {
                "format": "%(asctime)s.%(msecs)03d %(levelname)-7s %(name)s :\n  %(message)s",
                "datefmt": "%H:%M:%S",
            },
            "verbose": {
                "format": "%(asctime)s.%(msecs)03d %(levelname)-7s %(name)-20s %(filename)-15s %(funcName)30s() :\n  %(message)s",
                "datefmt": "%H:%M:%S",
            },
        },
        "handlers": {
            "normal_console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "normal",
            },
            "verbose_console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {"handlers": ["normal_console"], "level": "INFO"},
            "nautobot": {
                "handlers": ["verbose_console" if DEBUG else "normal_console"],
                "level": LOG_LEVEL,
            },
            "rq.worker": {
                "handlers": ["verbose_console" if DEBUG else "normal_console"],
                "level": LOG_LEVEL,
            },
        },
    }

#
# Redis
#

# The django-redis cache is used to establish concurrent locks using Redis. The
# django-rq settings will use the same instance/database by default.
#
# This "default" server is now used by RQ_QUEUES.
# >> See: nautobot.core.settings.RQ_QUEUES
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": parse_redis_connection(redis_database=0),
        "TIMEOUT": 300,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# RQ_QUEUES is not set here because it just uses the default that gets imported
# up top via `from nautobot.core.settings import *`.

# Redis Cacheops
CACHEOPS_REDIS = parse_redis_connection(redis_database=1)

#
# Celery settings are not defined here because they can be overloaded with
# environment variables. By default they use `CACHES["default"]["LOCATION"]`.
#

# Enable installed plugins. Add the name of each plugin to the list.
PLUGINS = ["nautobot_secrets_providers"]

# Plugins configuration settings. These settings are used by various plugins that the user may have installed.
# Each key in the dictionary is the name of an installed plugin and its value is a dictionary of settings.
# PLUGINS_CONFIG = {
#     'my_plugin': {
#         'foo': 'bar',
#         'buzz': 'bazz'
#     }
# }

PLUGINS_CONFIG = {
    "nautobot_secrets_providers": {
        "hashicorp_vault": {
            "url": os.environ.get("VAULT_URL", "http://vault:8200"),
            "token": os.environ.get("VAULT_TOKEN", "nautobot"),
        },
        "thycotic": {  # https://github.com/thycotic/python-tss-sdk
            "base_url": os.getenv("SECRET_SERVER_BASE_URL"),
            "cloud_based": is_truthy(os.getenv("SECRET_SERVER_IS_CLOUD_BASED", "False")),
            # tenant: required when cloud_based == True
            "tenant": os.getenv("SECRET_SERVER_TENANT", ""),
            # Setup thycotic authorizer
            # Username | Password | Token | Domain | Authorizer
            #   def    |   def    |   *   |   -    | PasswordGrantAuthorizer
            #   def    |   def    |   *   |  def   | DomainPasswordGrantAuthorizer
            #    -     |    -     |  def  |   *    | AccessTokenAuthorizer
            #   def    |    -     |  def  |   *    | AccessTokenAuthorizer
            #    -     |   def    |  def  |   *    | AccessTokenAuthorizer
            "username": os.getenv("SECRET_SERVER_USERNAME", ""),
            "password": os.getenv("SECRET_SERVER_PASSWORD", ""),
            "token": os.getenv("SECRET_SERVER_TOKEN", ""),
            "domain": os.getenv("SECRET_SERVER_DOMAIN", ""),
            # ca_bundle_path: (optional) Path to trusted certificates file.
            #     This must be set as environment variable.
            #     see: https://docs.python-requests.org/en/master/user/advanced/
            "ca_bundle_path": os.getenv("REQUESTS_CA_BUNDLE", ""),
        },
    },
}
