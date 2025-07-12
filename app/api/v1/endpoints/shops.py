from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List
from uuid import UUID
from app.db.session import get_session
from app.db.models.shop import Shop
from app.db.schemas.shop import ShopCreate, ShopRead, ShopUpdate

shop_router = APIRouter(prefix="/shops", tags=["Shops"])


@shop_router.post("/", response_model=ShopRead)
def create_shop(shop: ShopCreate, session: Session = Depends(get_session)):
    db_shop = Shop.model_validate(shop)
    session.add(db_shop)
    session.commit()
    session.refresh(db_shop)
    return db_shop


@shop_router.get("/", response_model=List[ShopRead])
def get_all_shops(session: Session = Depends(get_session)):
    shops = session.exec(select(Shop)).all()
    return shops


@shop_router.get("/nearby", response_model=List[ShopRead])
def get_nearby_shops(
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_meters: int = Query(5000),
    session: Session = Depends(get_session),
):
    query = f"""
    SELECT * FROM shop
    WHERE ST_DWithin(
        location, ST_SetSRID(ST_MakePoint(:lon, :lat), 4326)::geography, :radius
    )
    """
    result = session.exec(
        query, {"lon": longitude, "lat": latitude, "radius": radius_meters}
    )
    return result.all()


@shop_router.get("/{shop_id}", response_model=ShopRead)
def get_shop(shop_id: int, session: Session = Depends(get_session)):
    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    return shop


@shop_router.put("/{shop_id}", response_model=ShopRead)
def update_shop(
    shop_id: int,
    shop_data: ShopUpdate,
    session: Session = Depends(get_session),
):
    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    shop.sqlmodel_update(shop_data.model_dump(exclude_unset=True))
    session.add(shop)
    session.commit()
    session.refresh(shop)
    return shop


@shop_router.delete("/{shop_id}")
def delete_shop(shop_id: int, session: Session = Depends(get_session)):
    shop = session.get(Shop, shop_id)
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    session.delete(shop)
    session.commit()
    return {"detail": "Shop deleted"}
