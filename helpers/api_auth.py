from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyQuery


api_key_query_auth = APIKeyQuery(name="api_key", auto_error=True)

