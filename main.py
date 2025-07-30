from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.api.v1.endpoints.usersApi import user_router
from app.db.session import DataBasePool 
from app.api.v1.endpoints.shopsApi import shop_router 
from app.api.v1.endpoints.itemsApi import item_router 
from app.api.v1.endpoints.inventoryApi import inventory_router 
from app.api.v1.endpoints.searchApi import search_router 
from app.api.v1.endpoints.statusApi import status_router 
from app.core.typesense_client import create_collections


port = 8050

@asynccontextmanager
async def lifespan(app: FastAPI):
    await DataBasePool.setup()
    create_collections()
    yield
    await DataBasePool.teardown()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(shop_router)
app.include_router(item_router)
app.include_router(inventory_router)
app.include_router(search_router)
app.include_router(status_router)


@app.get("/")
def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
