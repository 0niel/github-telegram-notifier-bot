from typing import Optional

from pydantic import BaseModel

from github.models.user import User


class Issue(BaseModel):
    id: Optional[int]
    html_url: Optional[str]
    title: Optional[str]
    user: Optional[User]
