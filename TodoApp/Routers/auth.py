from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models import Users
from db import SessionLocal
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

#Authenticate the user and password
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True

@router.post("/auth/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, new_user: CreateUserRequest):
    create_user_model = Users(
        email = new_user.email,
        username = new_user.username,
        first_name = new_user.first_name,
        last_name = new_user.last_name,
        role=new_user.role,
        hashed_password = bcrypt_context.hash(new_user.password),
        is_active = True
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user: 
        return 'Authentication failed'
    return 'User authorised'
