from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infra.sql.users.users_model import UsersTable
from infra.schemas.user.user_schema import UserSchema
from infra.sql.database.database import get_db
from config.config import SECRET_KEY
from utils.logger.logger import logger
from utils.global_catch.global_catch import global_catch
from datetime import datetime, timezone, timedelta
import jwt
import bcrypt
#from passlib.context import CryptContext

user_authorization_router = APIRouter()

@user_authorization_router.post("/authorize", status_code=200)
@global_catch
async def UserAuth(user: UserSchema, db: Session = Depends(get_db)):
    login = user.login
    password = user.password
    #pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    #pwd_context.verify(password, hashed_password)
    potential_user = db.query(UsersTable).filter(UsersTable.login == login).first()
    hashed_password = potential_user.password
    if not potential_user:
        logger.info(f"User with login {login} doesn't exist. [400]")
        raise HTTPException(status_code=400, detail=f"User with the following login ({login}) doesn't exist!")
    if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode('utf-8')): # user.password = hashed password, will return true if password is correct
        expiration = datetime.now(timezone.utc) + timedelta(minutes=60)
        payload = {"user": login, "exp": expiration}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        logger.info(f"Login successfull [200]")
        return {"token": token}
    logger.info(f"Wrong password. [400]")
    raise HTTPException(status_code=400, detail=f"Wrong password!")