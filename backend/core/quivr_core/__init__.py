from importlib.metadata import entry_points

from .brain import Brain
from .chat_llm import ChatLLM
from .processor.registry import register_processor, registry

__all__ = ["Brain", "ChatLLM", "registry", "register_processor"]


def register_entries():
    if entry_points is not None:
        try:
            eps = entry_points()
        except TypeError:
            pass  # importlib-metadata < 0.8
        else:
            if hasattr(eps, "select"):  # Python 3.10+ / importlib_metadata >= 3.9.0
                processors = eps.select(group="quivr_core.processor")
            else:
                processors = eps.get("quivr_core.processor", [])
            registered_names = set()
            for spec in processors:
                err_msg = f"Unable to load processor from {spec}"
                name = spec.name
                if name in registered_names:
                    continue
                registered_names.add(name)
                register_processor(
                    name,
                    spec.value.replace(":", "."),
                    errtxt=err_msg,
                    append=True,
                )


register_entries()
