import os
from typing import Annotated

from fastapi import Depends
from logger import get_logger
from models.settings import common_dependencies

logger = get_logger(__name__)
