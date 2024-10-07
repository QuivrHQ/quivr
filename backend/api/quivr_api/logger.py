import logging
import os
import queue
import sys
import threading
from logging.handlers import RotatingFileHandler
from typing import List

import orjson
import requests
import structlog

from quivr_api.models.settings import parseable_settings

# Thread-safe queue for log messages
log_queue = queue.Queue()
stop_log_queue = threading.Event()


class ParseableLogHandler(logging.Handler):
    def __init__(
        self,
        base_parseable_url: str,
        auth_token: str,
        stream_name: str,
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
        self._worker_thread.daemon = True
        self._worker_thread.start()
        self.headers = {
            "Authorization": f"Basic {auth_token}",  # base64 encoding user:mdp
            "Content-Type": "application/json",
        }

    def emit(self, record: logging.LogRecord):
        # FIXME (@AmineDiro): This ping-pong of serialization/deserialization is a limitation of logging formatter
        # The formatter should return a 'str' for the logger to print
        if isinstance(record.msg, str):
            return
        elif isinstance(record.msg, dict):
            logger_name = record.msg.get("logger", None)
            if logger_name and (
                logger_name.startswith("quivr_api.access")
                or logger_name.startswith("quivr_api.error")
            ):
                url = record.msg.get("url", None)
                # Filter on healthz
                if url and "healthz" not in url:
                    fmt = orjson.loads(self.format(record))
                    log_queue.put(fmt)
        else:
            return

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


def extract_from_record(_, __, event_dict):
    """
    Extract thread and process names and add them to the event dict.
    """
    record = event_dict["_record"]
    event_dict["thread_name"] = record.threadName
    event_dict["process_name"] = record.processName
    return event_dict


def drop_http_context(_, __, event_dict):
    """
    Extract thread and process names and add them to the event dict.
    """
    keys = ["msg", "logger", "level", "timestamp", "exc_info"]
    return {k: event_dict.get(k, None) for k in keys}


def setup_logger(
    log_file="application.log", send_log_server: bool = parseable_settings.use_parseable
):
    structlog.reset_defaults()
    # Shared handlers
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.processors.EventRenamer("msg"),
    ]
    structlog.configure(
        processors=shared_processors
        + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        # Use standard logging compatible logger
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        # Use Python's logging configuration
        cache_logger_on_first_use=True,
    )
    # Set Formatters
    plain_fmt = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            extract_from_record,
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(
                colors=False, exception_formatter=structlog.dev.plain_traceback
            ),
        ],
    )
    color_fmt = structlog.stdlib.ProcessorFormatter(
        processors=[
            drop_http_context,
            structlog.dev.ConsoleRenderer(
                colors=True,
                exception_formatter=structlog.dev.RichTracebackFormatter(
                    show_locals=False
                ),
            ),
        ],
        foreign_pre_chain=shared_processors,
    )
    parseable_fmt = structlog.stdlib.ProcessorFormatter(
        processors=[
            # TODO: Which one gets us the better debug experience ?
            # structlog.processors.ExceptionRenderer(
            #     exception_formatter=structlog.tracebacks.ExceptionDictTransformer(
            #         show_locals=False
            #     )
            # ),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
        foreign_pre_chain=shared_processors
        + [
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
        ],
    )

    # Set handlers
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5000000, backupCount=5
    )  # 5MB file
    console_handler.setFormatter(color_fmt)
    file_handler.setFormatter(plain_fmt)
    handlers: list[logging.Handler] = [console_handler, file_handler]
    if (
        send_log_server
        and parseable_settings.parseable_url is not None
        and parseable_settings.parseable_auth is not None
        and parseable_settings.parseable_stream_name
    ):
        parseable_handler = ParseableLogHandler(
            auth_token=parseable_settings.parseable_auth,
            base_parseable_url=parseable_settings.parseable_url,
            stream_name=parseable_settings.parseable_stream_name,
        )
        parseable_handler.setFormatter(parseable_fmt)
        handlers.append(parseable_handler)

    # Configure logger
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = []
    for handler in handlers:
        root_logger.addHandler(handler)

    _clear_uvicorn_logger()


def _clear_uvicorn_logger():
    for _log in [
        "uvicorn",
        "httpcore",
        "uvicorn.error",
        "uvicorn.access",
        "urllib3",
        "httpx",
    ]:
        # Clear the log handlers for uvicorn loggers, and enable propagation
        # so the messages are caught by our root logger and formatted correctly
        # by structlog
        logging.getLogger(_log).setLevel(logging.WARNING)
        logging.getLogger(_log).handlers.clear()
        logging.getLogger(_log).propagate = True


setup_logger()


def get_logger(name: str | None = None):
    assert structlog.is_configured()
    return structlog.get_logger(name)
