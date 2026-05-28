from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    body: str
    author_id: int
    published: bool = False


class ArticleResponse(BaseModel):
    id: int
    title: str
    body: str
    author_id: int
    published: bool
