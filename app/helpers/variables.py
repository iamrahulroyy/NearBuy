from os import getenv
from typing import Literal
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL = getenv("DATABASE_URL", "")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables")
COOKIE_KEY: str = getenv("COOKIE_KEY", "nearbuy_auth_token")
TYPESENSE_HOST = getenv("TYPESENSE_HOST")
TYPESENSE_PORT = int(getenv("TYPESENSE_PORT", "8108"))
TYPESENSE_PROTOCOL = getenv("TYPESENSE_PROTOCOL")
TYPESENSE_API_KEY = getenv("TYPESENSE_API_KEY")
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = int(getenv("REDIS_PORT", "6379"))

# Production environment detection
# Set IS_PRODUCTION=true in your production environment variables
IS_PRODUCTION = getenv("IS_PRODUCTION", "false").lower() == "true"

# Cookie settings for cross-origin authentication
# In production (HTTPS + cross-origin), use secure=True and samesite="none"
# In development (localhost), use secure=False and samesite="lax"
COOKIE_SECURE: bool = IS_PRODUCTION
COOKIE_SAMESITE: Literal["lax", "strict", "none"] = "none" if IS_PRODUCTION else "lax"