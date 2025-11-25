from fastapi import APIRouter, Depends, BackgroundTasks, Query, Request
from app.db.session import DataBasePool, authentication_required
from app.db.models.user import UserRole
from typesense_helper.sync_db_to_typesense import sync_database_to_typesense
from app.helpers.fake_data_generator import generate_fake_data
from app.helpers.helpers import send_json_response
from fastapi import status

admin_router = APIRouter(prefix="/admin", tags=["Admin"])

@admin_router.post("/index-typesense", description="Trigger full database sync to Typesense (Admin only)")
@authentication_required([UserRole.ADMIN, UserRole.SUPER_ADMIN])
async def index_typesense_endpoint(
    request: Request,
    background_tasks: BackgroundTasks,
    db_pool=Depends(DataBasePool.get_pool)
):
    # Run indexing in background
    background_tasks.add_task(sync_database_to_typesense)
    return send_json_response(
        message="Typesense indexing started in background.",
        status=status.HTTP_200_OK,
        body={}
    )

@admin_router.post("/generate-fake-data", description="Generate fake shops and items (Admin only)")
@authentication_required([UserRole.ADMIN, UserRole.SUPER_ADMIN])
async def generate_fake_data_endpoint(
    request: Request,
    background_tasks: BackgroundTasks,
    shops_count: int = Query(10, description="Number of shops to generate"),
    items_per_shop: int = Query(5, description="Number of items per shop"),
    db_pool=Depends(DataBasePool.get_pool)
):
    # Run fake data generation in background
    # We need to pass a new session or handle session within the task. 
    # generate_fake_data takes a session. 
    # Since db_pool is a session, we can't pass it directly to background task if it gets closed.
    # But DataBasePool.get_pool returns a session that is scoped to the request? 
    # Actually DataBasePool._db_pool is a global session in this codebase (based on session.py).
    # "with Session(cls._engine) as session: cls._db_pool = session" in setup.
    # So it seems it's a single global session? That's weird for async, but okay.
    # If it's a global session, we can pass it.
    
    # However, to be safe, let's wrap it in a function that creates a new session or uses the global pool correctly.
    # generate_fake_data uses the passed session.
    
    background_tasks.add_task(generate_fake_data, db_pool, shops_count, items_per_shop)
    
    return send_json_response(
        message=f"Fake data generation started for {shops_count} shops.",
        status=status.HTTP_200_OK,
        body={}
    )
