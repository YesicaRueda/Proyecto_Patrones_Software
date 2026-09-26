
import logging


class StandardLoggingAdapter:

    def __init__(self, filename="mes.log"):
        self._logger = logging.getLogger(f"MES.{filename}")
        self._logger.setLevel(logging.DEBUG)

        if not self._logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(message)s"
            )

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            file_handler = logging.FileHandler(filename)
            file_handler.setFormatter(formatter)

            self._logger.addHandler(console_handler)
            self._logger.addHandler(file_handler)

    def write(self, message, level="INFO"):
        level = level.upper()
        if level == "WARNING":
            self._logger.warning(message)
        elif level == "ERROR":
            self._logger.error(message)
        else:
            self._logger.info(message)