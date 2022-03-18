from typing import Optional

from pydantic import BaseModel

from github.models.user import User


class Repository(BaseModel):
    id: Optional[int]
    name: Optional[str]
    full_name: Optional[str]
    html_url: Optional[str]
    stargazers_count: int
    watchers_count: int
    owner: Optional[User]
