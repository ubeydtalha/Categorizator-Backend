

from enum import Enum
import json
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field

from app.schemas.category import Category, CategorySync
from app.schemas.item import Item, ItemSync


class ActionType(Enum):
    ADD = "ADD"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    UNKNOWN = "UNKNOWN"

class DescriptionType(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    FETCH = "FETCH" # Fetching data from the server , id si olan ve veritabanında daha güncel olan veri , client fetch etmeli
    UNKNOWN = "UNKNOWN"

class SyncItemModel(BaseModel):
    action : Annotated[ActionType, Field(..., description="Action type to be performed on the item")]
    item :  Union[ItemSync,CategorySync]
    type : Literal["Item","Category"]
    is_synced : bool = False
    description : Annotated[DescriptionType, Field(..., description="Description of the sync action")] = DescriptionType.UNKNOWN

    async def from_json_text(json_text: str):
        data = json.loads(json_text)
        action = ActionType(data["action"])
        item = ItemSync.model_validate(data["item"]) if data["type"] == "Product" else Category.model_validate(data["item"])
        type = "Item" if data["type"] == "Product" else "Category"
        return SyncItemModel(action=action, item=item, type=type)
    



class ResponseItemModel(BaseModel):
    action : Annotated[ActionType, Field(..., description="Action type to be performed on the item")]
    item : Union[Item,Category]
    type : Literal["Item","Category"]
    is_synced : bool = False
    description : str = "Item not synced"

    def to_json_text(self):
        return json.dumps(self.model_dump_json()   )

    async def from_json_text(json_text: str):
        data = json.loads(json_text)
        action= ActionType(data["action"])
        item = Item.model_validate_strings(data["item"]) if data["type"] == "Item" else Category.model_validate_strings(data["item"])
        type = data["type"]
        return ResponseItemModel(action=action, item=item, type=type)