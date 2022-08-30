from typing import Union, List
from datetime import datetime, timedelta
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from utils.passlib_crypt import verify_password
from schemas.schemas import (
    User, UserInDB, AccessToken, TokenData, UserOut, UserChangePassword,
    RefreshToken, AccessRefreshToken)
from db.database import get_db
from crud.auth import UserCRUD


load_dotenv()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

# to get a string like this run: openssl rand -hex 32
# use scopes do fastapi.SecurityScopes para permissoes personalizadas
ACCESS_SECRET_KEY = os.getenv("ACCESS_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")


def get_user(username: str, db: Session):
    user = UserCRUD(db).obter(username)
    if user:
        return UserInDB(
            username = user.username,
            password = user.password,
            full_name = user.full_name,
            disabled = user.disabled
        )
    else:
        return False
        

def authenticate_user(username: str, password: str, db: Session):
    user = get_user(username, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=AccessRefreshToken, tags=["auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer", "username": user.username}


@router.post('/token/refresh', response_model=AccessToken, status_code=status.HTTP_201_CREATED, tags=["auth"])
def refresh_token(refresh: RefreshToken, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh.refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/users', response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["auth"])
def criar_user(user: UserInDB, db: Session = Depends(get_db)):
    user = UserCRUD(db).criar(user)
    return user

@router.get('/users', response_model=List[UserOut], tags=["auth"])
def listar_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return UserCRUD(db).listar()

@router.get('/users/{username}', response_model=UserOut, tags=["auth"],)
def obter_user(username: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    try:
        user = UserCRUD(db).obter(username)
        return user
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Não existe um usuario com username={username}'
        )

@router.put("/users/change_my_password", tags=["auth"])
async def atualizar_password_user(
    passwords: UserChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
    ):
    UserCRUD(db).atualizar_senha(current_user.username, passwords)
    return {"msg": "Senha alterada com sucesso"}

@router.delete('/users/{username}', tags=["auth"])
def remover_user(username: str, db: User = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    UserCRUD(db).remover(username)
    return {"msg": "Removido com sucesso"}
    