from enum import Enum


class RoleEnum(str, Enum):
    Viewer = "Viewer"
    Editor = "Editor"
    Owner = "Owner"
