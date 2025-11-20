"""Items domain dependencies."""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize rate limiter for items
limiter = Limiter(key_func=get_remote_address)
