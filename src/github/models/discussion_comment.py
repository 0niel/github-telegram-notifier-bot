from typing import Optional

from pydantic import BaseModel

from github.models.discussion import Discussion
from github.models.user import User


class DiscussionComment(BaseModel):
    id: Optional[int]
    html_url: Optional[str]
    body: Optional[str]
    user: Optional[User]
    discussion: Optional[Discussion]
