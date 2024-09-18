from copy import deepcopy
from typing import Any, Callable, Optional, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

Model = TypeVar("Model", bound=Type[BaseModel])


def all_optional(without_fields: list[str] | None = None) -> Callable[[Model], Model]:
    if without_fields is None:
        without_fields = []

    def wrapper(model: Type[Model]) -> Type[Model]:
        base_model: Type[Model] = model

        def make_field_optional(
            field: FieldInfo, default: Any = None
        ) -> tuple[Any, FieldInfo]:
            new = deepcopy(field)
            new.default = default
            new.annotation = Optional[field.annotation]
            return new.annotation, new

        if without_fields:
            base_model = BaseModel

        return create_model(
            model.__name__,
            __base__=base_model,
            __module__=model.__module__,
            **{
                field_name: make_field_optional(field_info)
                for field_name, field_info in model.model_fields.items()
                if field_name not in without_fields
            },
        )

    return wrapper


class Test(BaseModel):
    id: UUID
    name: Optional[str] = None


@all_optional()
class TestUpdate(Test):
    pass
