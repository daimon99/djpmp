# coding: utf-8
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s | %(levelname)s | %(name)s:%(lineno)s | %(funcName)s '
                      '| %(process)d | %(thread)d | %(threadName)s | %(message)s'
        },
        'simple': {
            'format': '%(asctime)s | %(levelname)s | %(name)s:%(lineno)s:%(funcName)s | %(message)s'
        },
        'dblog': {
            'format': '%(asctime)s | %(levelname)s | %(message)s'
        }
    },
    # 'filters': {
    #     'require_debug_true': {
    #         '()': 'django.utils.log.RequireDebugTrue',
    #     },
    # },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'db_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOG_DIR, 'db.log'),
            'formatter': 'dblog',
        },
        'app_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOG_DIR, 'app.log'),
            'formatter': 'verbose',
        },
        'sec_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(LOG_DIR, 'sec.log'),
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'app_file'],
        'level': 'INFO',
    },
    'loggers': {
        'django.db': {
            'handlers': ['db_file', ],
            'level': 'DEBUG',
            'propagate': False
        },
        'security': {
            'handlers': ['sec_file'],
            'level': 'INFO',
            'propagate': False
        },
        'djpmp': {
            'handlers': ['app_file', 'console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}
