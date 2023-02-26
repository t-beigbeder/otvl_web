import os

import uvicorn

from otvl_web import context


log_level = os.getenv("OTVL_WEB_LOGGING", "INFO")
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"handlers": ["default"], "level": log_level},
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "use_colors": None,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s - %(name)s - %(levelname)s - %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"handlers": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": False},
    },
}

ctx = context.Context()

if __name__ == "__main__":
    uvicorn.run("otvl_web.app:app", host=ctx.host, port=ctx.port, reload=ctx.reload,
                log_config=LOGGING_CONFIG, proxy_headers=True, forwarded_allow_ips="*",
                access_log=(not ctx.full_access_log))
