from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel
from common.enum import OrderDirection


class BaseModelDict(BaseModel):
    def dict(self, no_null: bool = False, keep_null_keys: Optional[List[str]] = []):
        def convert_item(item):
            if isinstance(item, dict):
                return {k: convert_item(v) for k, v in item.items()}
            elif isinstance(item, UUID):
                return str(item)
            elif isinstance(item, Enum):
                return item.value
            elif isinstance(item, datetime):
                return item.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(item, date):
                return item.strftime("%Y-%m-%d")
            elif isinstance(item, list):
                return [convert_item(i) for i in item]
            elif isinstance(item, BaseModelDict):
                return item.dict(no_null=no_null, keep_null_keys=keep_null_keys)
            else:
                return item

        d = self.model_dump()
        if no_null:
            return {
                k: convert_item(v)
                for k, v in d.items()
                if v is not None or k in keep_null_keys
            }
        return {k: convert_item(v) for k, v in d.items()}


class ErrorResponse(BaseModel):
    message: Optional[str]
