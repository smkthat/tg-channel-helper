import asyncio

from app.configuration.log import get_logger
from app.loader import start_app

LOGGER = get_logger(__name__, 'logs')


def main():
    try:
        LOGGER.info("start application")
        asyncio.run(start_app())
    except (
            RuntimeError,
            KeyboardInterrupt,
            SystemExit,
            AttributeError,
            FileNotFoundError
    ) as exc:
        LOGGER.error(exc)
        LOGGER.warning("Exit")


if __name__ == "__main__":
    main()
