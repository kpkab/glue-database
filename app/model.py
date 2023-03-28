from pydantic import BaseModel


class Glue_database(BaseModel):
    Name: str
    Description: str