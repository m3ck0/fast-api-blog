from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    title: str
    content: str
    publish_at_ts: float
    is_published: bool = True


class PostResponse(BaseModel):
    id: str
    title: str
    content: str
    is_published: bool
