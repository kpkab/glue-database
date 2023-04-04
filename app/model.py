from typing import Union

from pydantic import BaseModel, Field


class Glue_database(BaseModel):
    Name: str = Field(min_length=1, max_length=255)
    Description: str


class SuccessResponse(BaseModel):
    success: bool = True
    status: int = 200
    data: Union[None, dict, list] = None


class ErrorResponse(BaseModel):
    success: bool = False
    status: int = 404
    message: Union[None, dict, list] = {"message": "Something wrong"}


class ExceptionResponse(BaseModel):
    success: bool = False
    status: int = 404
    message: Union[None, dict, list] = {"message": "Unhandled Exception"}
