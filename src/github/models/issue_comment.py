from typing import Optional

from pydantic import BaseModel

from github.models.user import User


class IssueComment(BaseModel):
    id: Optional[int]
    html_url: Optional[str]
    issue_url: Optional[str]
    user: Optional[User]
    body: Optional[str]

