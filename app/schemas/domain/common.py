
from typing import Optional
from schemas.base import BaseModelDict

from common.enum import OrderDirection


class QueryBase(BaseModelDict):
    page: int
    limit: int
    order_by: Optional[str]
    order_direction: Optional[OrderDirection]

