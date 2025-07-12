from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.db.session import engine
from app.api.v1.endpoints.users import user_router 
from app.api.v1.endpoints.shops import shop_router 
from app.api.v1.endpoints.items import item_router 
from app.api.v1.endpoints.inventory import inventory_router 
from app.api.v1.endpoints.search import search_router 
from app.api.v1.endpoints.status import status_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
