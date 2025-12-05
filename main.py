from fastapi import FastAPI
from contextlib import asynccontextmanager
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
from app.api.v1.endpoints.vendorApi import vendor_router
from app.api.v1.endpoints.categoriesApi import categories_router
from app.api.v1.endpoints.shopsListApi import shops_list_router
from app.api.v1.endpoints.adminApi import admin_router
from app.api.v1.endpoints.analyticsApi import router as analytics_router
from typesense_helper.typesense_client import create_collections
from fastapi.middleware.cors import CORSMiddleware


port = 8050


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DataBasePool.setup()
    try:
        create_collections()
    except Exception as e:
        print(f"Warning: Could not connect to Typesense: {e}")
    yield
    await DataBasePool.teardown()


app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost:3000",  # Next.js default port
    "http://localhost:5173",  # Vite default port
    "http://localhost:8000",
    "http://localhost:8050",  # Backend port
    "http://10.0.0.167:8050",
    "http://10.0.0.204:8000",
    # For development: allow any localhost port
    "http://127.0.0.1:3000",
    "https://near-buy-two.vercel.app/",
    "https://near-buy-two.vercel.app",
    "https://nearbuy.firebit.in/",
    "https://nearbuy.firebit.in",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

app.include_router(user_router, prefix="/api/v1")
app.include_router(shop_router, prefix="/api/v1")
app.include_router(item_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")
app.include_router(search_router, prefix="/api/v1")
app.include_router(status_router, prefix="/api/v1")
app.include_router(vendor_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1/categories")
app.include_router(shops_list_router, prefix="/api/v1/public/shops")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1/analytics")


@app.get("/")
def root():
    return {"message": "API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
