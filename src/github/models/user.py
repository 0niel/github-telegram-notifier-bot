from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    login: Optional[str]
    name: Optional[str]
    email: Optional[str]
    html_url: Optional[str]
