from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.api.v1.endpoints.usersApi import user_router
from app.core.limiter import limiter 
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.db.session import DataBasePool 
from app.api.v1.endpoints.shopsApi import shop_router 
from app.api.v1.endpoints.itemsApi import item_router 
from app.api.v1.endpoints.inventoryApi import inventory_router 
from app.api.v1.endpoints.searchApi import search_router 
from app.api.v1.endpoints.statusApi import status_router
from typesense_helper.typesense_client import create_collections 
from fastapi.middleware.cors import CORSMiddleware


port = 8059

@asynccontextmanager
async def lifespan(app: FastAPI):
    await DataBasePool.setup()
    create_collections()
    yield
    await DataBasePool.teardown()


app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(user_router, prefix="/api/v1")
app.include_router(shop_router, prefix="/api/v1")
app.include_router(item_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(status_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
