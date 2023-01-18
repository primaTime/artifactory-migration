from typing import TypedDict
from schema.ListItemResponse import ListItemResponse

class StorageResponse(TypedDict):
    path: str
    children: list[ListItemResponse]
    uri: str
    created: str