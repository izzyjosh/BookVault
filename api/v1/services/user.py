import os
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from pydantic import EmailStr
from datetime import datetime, timezone, timedelta
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from api.v1.schemas.user import UserCreateSchema, UserResponseSchema
from api.v1.models.user import User
from api.v1.models.access_token import AccessToken

load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")
hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))


class UserService:

    def verify_password(self, plain_password: str, hashed_password: str):
        return hash_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str):
        return hash_context.hash(password)

    def generate_access_token(self, db: Session, user: User):
        payload = {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
        }

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload.update({"exp": expire})
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        access_token = AccessToken(user_id=user.id, token=token, expiry_time=expire)

        db.add(access_token)
        db.commit()
        db.refresh(access_token)

        return {"token": token, "expiry_time": expire}

    def user_exist(self, db: Session, email: str, username: str):
        check_user_email = db.query(User).filter(User.email == email).first()

        if check_user_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exist"
            )

        check_username = db.query(User).filter(User.username == username).first()

        if check_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exist"
            )

        return False

    def create_user(self, db: Session, schema: UserCreateSchema):

        user_exist = self.user_exist(
            db=db, email=schema.email, username=schema.username
        )

        # Password hashing

        hashed_password = self.hash_password(schema.password)
        schema.password = hashed_password
        user = User(**schema.model_dump())

        db.add(user)
        db.commit()

        access_token = self.generate_access_token(db=db, user=user)

        db.refresh(user)

        response = {
            "access_token": access_token["token"],
            "expiry_time": access_token["expiry_time"],
            "user": UserResponseSchema(**jsonable_encoder(user)),
        }

        return response

    def handle_login(self, db: Session, email: EmailStr, password: str):

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )

        # Verify password

        verify_password = self.verify_password(password, user.password)

        if not verify_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )

        # generate access token

        access_token, expiry = self.generate_access_token(db, user).values()

        # update last login

        user.last_login = datetime.now(timezone.utc)

        db.commit()
        db.refresh(user)

        response = {
            "access_token": access_token,
            "expiry_time": expiry,
            "user": UserResponseSchema(**jsonable_encoder(user)),
        }

        return response


user_service = UserService()
