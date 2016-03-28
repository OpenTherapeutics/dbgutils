DEBUG_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s:%(name)s:%(asctime)s:%(pathname)s:%(lineno)d %(message)s',
            'datefmt': '%Y%m%dT%H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'class': 'logging.StreamHandler',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
        }
    }
}