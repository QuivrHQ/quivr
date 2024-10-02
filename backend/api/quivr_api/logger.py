import logging
import os
import queue
import sys
import threading
from logging.handlers import RotatingFileHandler
from time import sleep
from typing import List

import orjson
import requests
import structlog
from pythonjsonlogger import jsonlogger

from quivr_api.models.settings import parseable_settings

# Thread-safe queue for log messages
log_queue = queue.Queue()
stop_log_queue = threading.Event()


class ParseableLogHandler(logging.Handler):
    def __init__(
        self,
        base_parseable_url: str,
        auth_token: str,
        stream_name: str = "quivr-api",
        batch_size: int = 10,
        flush_interval: float = 1,
    ):
        super().__init__()
        self.base_url = base_parseable_url
        self.stream_name = stream_name
        self.url = self.base_url + self.stream_name
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self._worker_thread = threading.Thread(target=self._process_log_queue)
        self._worker_thread.start()
        self.headers = {
            "Authorization": f"Basic {auth_token}",  # base64 encoding user:mdp
            "Content-Type": "application/json",
        }

    def emit(self, record: logging.LogRecord):
        # NOTE (@AmineDiro): This ping-pong of serialization/deserialization is a limitation of logging formatter
        # The formatter should return a 'str' for the logger to print
        # We
        fmt = orjson.loads(self.format(record))
        log_queue.put(fmt)

    def _process_log_queue(self):
        """Background thread that processes the log queue and sends logs to Parseable."""
        logs_batch = []
        while not stop_log_queue.is_set():
            try:
                # Collect logs for batch processing
                log_data = log_queue.get(timeout=self.flush_interval)
                logs_batch.append(log_data)

                # Send logs if batch size is reached
                if len(logs_batch) >= self.batch_size:
                    self._send_logs_to_parseable(logs_batch)
                    logs_batch.clear()

            except queue.Empty:
                # If the queue is empty, send any remaining logs
                if logs_batch:
                    self._send_logs_to_parseable(logs_batch)
                    logs_batch.clear()

    def _send_logs_to_parseable(self, logs: List[str]):
        payload = orjson.dumps(logs)
        try:
            response = requests.post(self.url, headers=self.headers, data=payload)
            if response.status_code != 200:
                print(f"Failed to send logs to Parseable server: {response.text}")
        except Exception as e:
            print(f"Error sending logs to Parseable: {e}")

    def stop(self):
        """Stop the background worker thread and process any remaining logs."""
        stop_log_queue.set()
        self._worker_thread.join()
        # Process remaining logs before shutting down
        remaining_logs = list(log_queue.queue)
        if remaining_logs:
            self._send_logs_to_parseable(remaining_logs)


def get_logger(
    logger_name,
    log_file="application.log",
):
    log_level = os.getenv("LOG_LEVEL", "WARNING").upper()
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    logger.propagate = False

    # Set handlers
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5000000, backupCount=5
    )  # 5MB file

    handlers = [console_handler]

    if (
        parseable_settings.parseable_url is not None
        and parseable_settings.parseable_auth is not None
    ):
        parseable_handler = ParseableLogHandler(
            auth_token=parseable_settings.parseable_auth,
            base_parseable_url=parseable_settings.parseable_url,
        )
        handlers.append(parseable_handler)

    if not logger.handlers:
        for handler in handlers:
            handler.setFormatter(jsonlogger.JsonFormatter())
            logger.addHandler(handler)

    return logger


structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.EventRenamer("msg"),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),  # Use standard logging compatible logger
    wrapper_class=structlog.stdlib.BoundLogger,  # Use BoundLogger for compatibility
    # Use Python's logging configuration
    cache_logger_on_first_use=True,
)


def extract_from_record(_, __, event_dict):
    """
    Extract thread and process names and add them to the event dict.
    """
    record = event_dict["_record"]
    event_dict["thread_name"] = record.threadName
    event_dict["process_name"] = record.processName
    return event_dict


# Set handlers
console_handler = logging.StreamHandler(sys.stdout)
file_handler = RotatingFileHandler(
    "application.log", maxBytes=5000000, backupCount=5
)  # 5MB file

plain_fmt = structlog.stdlib.ProcessorFormatter(
    processors=[
        extract_from_record,
        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
        structlog.dev.ConsoleRenderer(colors=True),
    ],
)

console_handler.setFormatter(plain_fmt)
handlers: list[logging.Handler] = [console_handler]

if (
    parseable_settings.parseable_url is not None
    and parseable_settings.parseable_auth is not None
):
    parseable_fmt = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.processors.dict_tracebacks,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
        foreign_pre_chain=[
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
        ],
    )
    parseable_handler = ParseableLogHandler(
        auth_token=parseable_settings.parseable_auth,
        base_parseable_url=parseable_settings.parseable_url,
    )
    parseable_handler.setFormatter(parseable_fmt)
    handlers.append(parseable_handler)

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
quivr_logger = logging.getLogger("quivr-api")
quivr_logger.setLevel(log_level)
for handler in handlers:
    quivr_logger.addHandler(handler)

log = structlog.get_logger("quivr-api")

for _ in range(10):
    log.info("this is a test", a=12, b=121)
    try:
        a = 1 / 0
    except Exception as e:
        log.exception(f"error occured: {e}")
    sleep(0.4)
