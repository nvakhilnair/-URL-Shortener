import logging


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Configure the logger
            cls._instance.logger = logging.getLogger(__name__)
            cls._instance.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            # Add a console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            cls._instance.logger.addHandler(console_handler)
        return cls._instance
