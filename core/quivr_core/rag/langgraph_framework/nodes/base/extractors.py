"""
Configuration extraction interfaces and implementations.
Allows nodes to receive config extractors that know how to navigate different config structures.
"""

from typing import Dict, Any, Callable, Tuple, Union

# Config extractor can return a single config dict or tuple of config dicts
ConfigExtractor = Callable[
    [Dict[str, Any]], Union[Dict[str, Any], Tuple[Dict[str, Any], ...]]
]
