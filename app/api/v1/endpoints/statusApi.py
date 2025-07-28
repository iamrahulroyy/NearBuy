from fastapi import APIRouter, Request
from app.helpers.helpers import send_json_response
import time

status_router = APIRouter(prefix="/status", tags=["Status"])

@status_router.get("/health", description="Public health check endpoint")
async def health_check():
    return send_json_response(message="OK",status=200,body={"status": "healthy", "timestamp": int(time.time())})

@status_router.get("/info", description="Public app info endpoint")
async def app_info():
    return send_json_response(message="App Info",status=200,body={"app": "NearBuy API","version": "1.0.0","docs": "/docs"})

#other status/statistics endpoints in future!
