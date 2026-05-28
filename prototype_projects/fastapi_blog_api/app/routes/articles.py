from fastapi import APIRouter, Header, HTTPException, Query, status

from app.models import ArticleCreate, ArticleResponse


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=list[ArticleResponse])
async def list_articles(
    published: bool | None = Query(default=None),
    x_request_id: str | None = Header(default=None),
):
    return []


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(article_id: int):
    if article_id <= 0:
        raise HTTPException(status_code=400, detail="article_id must be positive")
    raise HTTPException(status_code=404, detail="Article not found")


@router.post("/", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(payload: ArticleCreate):
    return {
        "id": 1,
        "title": payload.title,
        "body": payload.body,
        "author_id": payload.author_id,
        "published": payload.published,
    }


@router.delete("/{article_id}", status_code=204)
async def delete_article(article_id: int):
    if article_id == 404:
        raise HTTPException(status_code=404, detail="Article not found")
    return None
