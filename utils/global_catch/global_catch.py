from functools import wraps
from fastapi import HTTPException
from utils.logger.logger import logger
import uuid


def global_catch(f):
  @wraps(f)
  async def decorator(*args, **kwargs):
    try:
      return await f(*args, **kwargs)
    except:
      error_id = uuid.uuid4()
      logger.exception(f"Unhandled exception. Error ID: {error_id}")
      raise HTTPException(
                status_code=400,
                detail=f"Application failed with an unhandled exception. Contact support. Error ID: {error_id}",
            )
  return decorator