from typing import Optional

from fastapi import HTTPException
from schemas.dto.common import ListRequestBase

from common.enum import OrderDirection


async def common_list_request_params(
    page: int = 1,
    limit: int = 10,
    order_by: Optional[str] = None,
    order_direction: Optional[OrderDirection] = None,
) -> ListRequestBase:

    if (order_by is None and order_direction is not None) or (
        order_by is not None and order_direction is None
    ):
        raise HTTPException(
            status_code=400, detail="Both sorting options must be provided"
        )

    if page < 1:
        raise HTTPException(status_code=400, detail="Page should not be lower than 1")
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit should not be lower than 1")

    return ListRequestBase(
        page=page, limit=limit, order_by=order_by, order_direction=order_direction
    )

