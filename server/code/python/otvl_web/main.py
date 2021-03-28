import os

import uvicorn

from otvl_web import context


LOGGING_CONFIG = dict(
        version=1,
        disable_existing_loggers=False,

        root={"level": os.getenv("OTVL_WEB_LOGGING", "INFO"), "handlers": ["console"]},
        loggers={
            "gunicorn.error": {
                "level": "INFO",
                "handlers": ["error_console"],
                "propagate": True,
                "qualname": "gunicorn.error"
            },

            "gunicorn.access": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": True,
                "qualname": "gunicorn.access"
            }
        },
        handlers={
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": "ext://sys.stdout"
            },
            "error_console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": "ext://sys.stderr"
            },
        },
        formatters={
            "generic": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "[%Y-%m-%d %H:%M:%S]",
                "class": "logging.Formatter"
            }
        }
)
ctx = context.Context()

if __name__ == '__main__':
    uvicorn.run('otvl_web.app:app', host=ctx.host, port=ctx.port, reload=ctx.reload,
                log_config=LOGGING_CONFIG)
