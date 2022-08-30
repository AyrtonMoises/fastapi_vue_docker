from sqlalchemy import delete
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.auth import User
from utils.passlib_crypt import verify_password, get_password_hash
from schemas import schemas


class UserCRUD():

    def __init__(self, db: Session):
        self.db = db

    def criar(self, user: schemas.User):
        user_exist = self.db.query(User).filter(User.username==user.username).one_or_none()

        if user_exist:
            raise HTTPException(status_code=404, detail="username existe")

        db_user = User(**user.dict())
        db_user.password = get_password_hash(user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user

    def atualizar_senha(self, username: str, passwords: schemas.UserChangePassword):
        user = self.db.query(User).filter(User.username==username).one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="username não existe")

        if not verify_password(passwords.old_password, user.password):
            raise HTTPException(status_code=404, detail="old_password incorreto")

        user.password = get_password_hash(passwords.new_password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def listar(self):
        user = self.db.query(User).all()
        return user

    def obter(self, username: str):
        user = self.db.query(User).filter(User.username==username).one_or_none()
        return user

    def remover(self, username: str):
        user_exist = self.db.query(User).filter(User.username==username).one_or_none()

        if user_exist is None:
            raise HTTPException(status_code=404, detail="username não existe")

        stmt = delete(User).where(User.username == username)
        self.db.execute(stmt)
        self.db.commit()