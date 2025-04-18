# logging_config.py
import os
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define log directory path
log_dir = os.path.join(BASE_DIR, 'logs')

# Ensure the log directory exists
os.makedirs(log_dir, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {name}: {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'rotating_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'app.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['rotating_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'slotbot': {
            'handlers': ['console', 'rotating_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
