import json
import logging
import os
import queue
import threading
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from typing import List

import requests
from colorlog import ColoredFormatter
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
        # Put the log record in the queue
        log_entry = self.format(record)

        # Get all standard LogRecord fields
        standard_fields = set(vars(logging.makeLogRecord({})))
        # Get all fields from the record
        all_fields = record.__dict__

        # Extract the 'extra' fields (the ones not in standard fields)
        log_extra_fields = {
            k: v for k, v in all_fields.items() if k not in standard_fields
        }

        log_data = {
            "id": record.thread,
            "datetime": datetime.now(timezone.utc).strftime("%d/%b/%Y:%H:%M:%S %z"),
            "log_level": record.levelname,
            "message": log_entry,
            **log_extra_fields,
        }

        log_queue.put(log_data)

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
        payload = json.dumps(logs)
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
    logger.propagate = False  # Prevent log propagation to avoid double logging

    formatter = logging.Formatter(
        "[%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s"
    )

    color_formatter = ColoredFormatter(
        "%(log_color)s[%(levelname)s]%(reset)s %(name)s [%(filename)s:%(lineno)d]: %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        reset=True,
        style="%",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(color_formatter)

    file_handler = RotatingFileHandler(
        log_file, maxBytes=5000000, backupCount=5
    )  # 5MB file
    file_handler.setFormatter(formatter)

    json_formatter = jsonlogger.JsonFormatter()

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        if (
            parseable_settings.parseable_url is not None
            and parseable_settings.parseable_auth is not None
        ):
            parseable_handler = ParseableLogHandler(
                auth_token=parseable_settings.parseable_auth,
                base_parseable_url=parseable_settings.parseable_url,
            )
            parseable_handler.setLevel(log_level)
            parseable_handler.setFormatter(json_formatter)
            logger.addHandler(parseable_handler)

    return logger
