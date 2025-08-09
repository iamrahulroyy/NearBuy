from os import getenv
from dotenv import load_dotenv

load_dotenv(override=True)

DATABASE_URL = getenv("DATABASE_URL")
COOKIE_KEY = getenv("COOKIE_KEY")
TYPESENSE_HOST = getenv("TYPESENSE_HOST")
TYPESENSE_PORT = int(getenv("TYPESENSE_PORT"))
TYPESENSE_PROTOCOL = getenv("TYPESENSE_PROTOCOL")
TYPESENSE_API_KEY = getenv("TYPESENSE_API_KEY")
REDIS_HOST = getenv("REDIS_HOST")
REDIS_PORT = int(getenv("REDIS_PORT"))