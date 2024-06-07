from datetime import datetime


def parse_message_time(message_time_str):
    return datetime.strptime(message_time_str, "%Y-%m-%dT%H:%M:%S.%f")
