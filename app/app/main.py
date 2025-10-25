from typing import Union
from fastapi import FastAPI, Query, HTTPException
from contextlib import asynccontextmanager
import asyncpg

DATABASE_URL = "postgresql://demo:test1234@db:5432/demo_development"

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)
    try:
        yield
    finally:
        await app.state.db_pool.close()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/materials")
async def get_materials(
        category: str | None = Query(default=None, description="過濾材料類別")
):
    try:
        async with app.state.db_pool.acquire() as conn:
            if category:
                rows = await conn.fetch(
                    "SELECT * FROM materials WHERE category = $1",
                    category
                )
            else:
                rows = await conn.fetch("SELECT * FROM materials")

            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))