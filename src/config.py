import logging.config


def is_local(env):
    """Return True if we're running in a local env, otherwise False"""
    return env.get('ENV', 'local') == 'local'


def get_eventstore_config(env):
    return {
        'host': env.get('DATA_RIVER_EVENTSTORE_HOST', 'eventstore'),
        'port': env.get('DATA_RIVER_EVENTSTORE_PORT', '1113'),
        'username': env.get('DATA_RIVER_EVENTSTORE_USERNAME', 'admin'),
        'password': env.get('DATA_RIVER_EVENTSTORE_PASSWORD', 'changeit'),
        'subscription': env.get('DATA_RIVER_EVENTSTORE_SUBSCRIPTION', 'datariver'),

        'streams': [
            {
                'name': '$ce-order',
                'events': ['refund_applied']
            },
            {
                'name': '$ce-purchase_order',
                'events': [
                    'quantity_moved_in_to_new_po',
                    'etd_eta_changed',
                    'purchase_order_approved'
                ]
            },
        ]
    }


def select_formatter(env):
    formatter = env.get('DATA_RIVER_LOGGING_FORMATTER', None)
    if formatter == 'plain':
        return 'plain_text'
    if formatter == 'logstash':
        return 'logstash'

    if is_local(env):
        return 'plain_text'
    return 'logstash'


def configure_logging(env=None):
    logging.config.dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'root': {
                'level': 'INFO',
                'handlers': ['default']
            },
            'formatters': {
                'plain_text': {
                    'format': '%(asctime)s %(levelname)s %(message)s',
                    'datefmt': '%H:%M:%S'
                },
                'logstash': {
                    '()': 'logstash_formatter.LogstashFormatter'
                }
            },
            'handlers': {
                'default': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://sys.stdout',
                    'formatter': select_formatter(env),
                    'level': 'NOTSET'
                }
            }
        }
    )
