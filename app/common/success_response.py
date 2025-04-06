from pydantic import BaseModel


class SuccessResponse(BaseModel):
    message: str

    class Config:
        json_schema_extra = {"example": {"message": "Success"}}