from datetime import datetime
from pydantic import BaseModel


class File(BaseModel):
    name: str
    uploaded: datetime
    expired: datetime
