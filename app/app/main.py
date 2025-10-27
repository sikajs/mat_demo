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
        category: str | None = Query(default=None, description="過濾材料類別"),
        usage_process: str | None = Query(default=None, description="製程"),
        limit: int = Query(500, ge=1, le=1000)
):

    query = "SELECT * FROM materials WHERE 1=1"
    params = []
    param_index = 1
    if category:
        query += f" AND category=${param_index}"
        params.append(category)
        param_index += 1
    if usage_process:
        query += f" AND usage_process=${param_index}"
        params.append(usage_process)
        param_index += 1

    query += f" LIMIT ${param_index}"
    params.append(limit)

    try:
        async with app.state.db_pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [dict(row) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))