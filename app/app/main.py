from typing import Union
from fastapi import FastAPI
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
async def get_materials():
    async with app.state.db_pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM materials")
        results = [dict(row) for row in rows]
        return results