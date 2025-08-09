from slowapi import Limiter
from slowapi.util import get_remote_address

# This creates a limiter that identifies users by their IP address.
limiter = Limiter(key_func=get_remote_address)