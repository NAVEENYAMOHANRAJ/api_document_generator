from fastapi import FastAPI

from app.routes import articles


app = FastAPI(title="Blog API")

app.include_router(articles.router, prefix="/api/v1")


@app.get("/health", tags=["system"])
async def health_check():
    return {"status": "ok"}
