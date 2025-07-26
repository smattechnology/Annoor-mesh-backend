from typing import Optional

from pydantic import BaseModel

class MessSchema(BaseModel):
    name:str
    address:str
    phone:Optional[str] = None