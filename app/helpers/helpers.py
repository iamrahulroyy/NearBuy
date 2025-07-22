import logging
import secrets
import uuid
from fastapi import Request
from pydantic import BaseModel
from typing import Any, Dict, Optional
import http.cookies
from ua_parser import user_agent_parser
from fastapi.responses import JSONResponse
from typing import Any, Dict

from app.helpers import variables



class ApiReqData(BaseModel):
    ip: Optional[str]
    country: Optional[str]
    origin: Optional[str]
    referer: Optional[str]
    browser: Optional[str]
    os: Optional[str]
    sessionID: Optional[str]


def generate_secure_random_number():
    """Generate cryptographical 4 digit random number"""
    randNum = secrets.randbelow(9000) + 1000
    return randNum


def get_user_agent_details(user_agent):
    parsed_data = user_agent_parser.Parse(user_agent)
    browser_name = parsed_data["user_agent"]["family"]
    browser_major_version = parsed_data["user_agent"]["major"]
    browser_info = f"{browser_name} {browser_major_version}"
    os_name = parsed_data["os"]["family"]
    os_major_version = parsed_data["os"]["major"]
    os_info = f"{os_name} {os_major_version}"
    return browser_info, os_info


async def get_fastApi_req_data(request: Request) -> ApiReqData:
    headers = request.headers
    # ip = request.client.host
    # print(f"HEADERS :: {headers}")
    # print(f"IP :: {headers}")
    cfip = headers.get("cf-connecting-ip", "")
    ip = headers.get("x-real-ip")
    country = headers.get("cf-ipcountry", "")
    origin = headers.get("origin")
    referer = headers.get("referer")
    ua = get_user_agent_details(headers.get("user-agent"))
    cookie = headers.get("cookie")
    sessionID = None

    if cookie:
        cookie_dict = http.cookies.SimpleCookie(cookie)
        sessionID = (
            cookie_dict.get(variables.COOKIE_KEY).value
            if variables.COOKIE_KEY in cookie_dict
            else None
        )

    return ApiReqData(
        ip=cfip or ip,
        country=country,
        origin=origin,
        referer=referer,
        browser=ua[0],
        os=ua[1],
        sessionID=sessionID,
    )


def send_json_response(
    message: str,
    status: int = 200,
    body: Any = None,
    additional_data: Dict[str, Any] = None,
) -> JSONResponse:
    """
    A reusable utility function for creating JSON responses in FastAPI.

    :param message: A message to include in the response (e.g., success/failure message).
    :param status: HTTP status code (default: 200).
    :param body: The response body (default: None).
    :param additional_data: A dictionary of additional data to include in the response (default: None).
    :return: A JSONResponse object with the provided data.

    ```python
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/user_plans")
    async def get_user_plans():
        # Assume serialized_cur_user_plans is your data
        serialized_cur_user_plans = {"plan": "Basic", "valid_until": "2025-01-01"}

        return create_json_response(
            message="Fetched User plans",
            status=200,
            body=serialized_cur_user_plans
        )

    ```
    """
    response_content = {"message": message, "status": status, "body": body}

    if additional_data:
        response_content.update(additional_data)
    return JSONResponse(content=response_content, status_code=status)


def generate_unique_id(length: int = 8) -> str:
    """
    Generates a random unique string using the secrets module.

    Args:
        length (int): The length of the unique ID in bytes. Defaults to 16.

    Returns:
        str: A random unique string of hexadecimal characters.
    """
    return secrets.token_hex(length)


def recursive_to_str(obj):
    if isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, list):
        return [recursive_to_str(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: recursive_to_str(v) for k, v in obj.items()}
    else:
        return obj

def extract_model(obj):
    # If it's a tuple (row), return first element, else as is
    if isinstance(obj, tuple):
        return obj[0]
    return obj
