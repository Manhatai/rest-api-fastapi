from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from infra.sql.users.users_model import UsersTable
from infra.schemas.user.user_schema import UserSchema
from infra.sql.database.database import get_db
from utils.logger.logger import logger
from utils.global_catch.global_catch import global_catch
import bcrypt

user_registration_router = APIRouter()

@user_registration_router.post("/authorize/register", status_code=201)
@global_catch
async def RegisterUser(user: UserSchema, db: Session = Depends(get_db)):
    login = user.login
    password = user.password
    potential_user = db.query(UsersTable).filter(UsersTable.login == login).first()
    if potential_user is not None:
        logger.info(f"User with login {login} already exists. [400]")
        raise HTTPException(status_code=400, detail=f"The following login ({login}) already exists!")
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) # .encode for converting string into bytes
    new_user = UsersTable(login=login, password=hashed.decode('utf-8')) # .decode bytes back to string
    db.add(new_user)
    db.commit()
    logger.info(f"POST for user ID {new_user.id} successfully. [201]")
    return f'New user {user.login} created.'