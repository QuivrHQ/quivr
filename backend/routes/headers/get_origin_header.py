from typing import Optional

from fastapi import Header


def get_origin_header(origin: Optional[str] = Header(None)):
    return origin
