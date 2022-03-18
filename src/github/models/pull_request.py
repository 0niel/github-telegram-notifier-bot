from typing import Optional

from pydantic import BaseModel

from github.models.user import User

class PullRequest(BaseModel):
    id: Optional[int]
    html_url: Optional[str]
    user: Optional[User]
    title: Optional[str]
