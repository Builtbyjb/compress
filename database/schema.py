from pydantic import BaseModel


class File(BaseModel):
    name: str
    uploaded: str
    expired: str
