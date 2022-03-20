from typing import Optional

from pydantic import BaseModel


class Label(BaseModel):
    id: Optional[int]
    url: Optional[str]
    name: Optional[str]
    color: Optional[str]
