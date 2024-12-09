from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from utils.logger.logger import logger
import jwt
from config.config import SECRET_KEY

class TokenBearer(HTTPBearer): # https://fastapi.tiangolo.com/reference/security/#fastapi.security.HTTPBearer, https://www.youtube.com/watch?v=9mx6LojqNCQ
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        try:
            jwt.decode(creds.credentials, SECRET_KEY, algorithms=["HS256"])
        except Exception:
            logger.info("Invalid token. [400]")
            raise HTTPException(status_code=400, detail="Invalid token")