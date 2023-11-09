from pydantic import BaseModel


class CreatePostRequest(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    id: str
    title: str
    content: str
