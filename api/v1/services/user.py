import os
import smtplib
import pyotp
from typing import Annotated
from email.mime.text import MIMEText
from fastapi import HTTPException, status, Depends, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
from pydantic import EmailStr, UUID4
from datetime import datetime, timezone, timedelta
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from api.v1.schemas.user import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from api.v1.models.user import User
from api.v1.models.otp import Otp
from api.v1.models.access_token import AccessToken
from api.v1.utils.dependencies import get_db

load_dotenv()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/account/login")
hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Email env variables
SENDER = os.environ.get("EMAIL_HOST_USER")
PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")


class UserService:
    def verify_otp_code(self, db: Session, code: int):
        otp = db.query(Otp).filter(Otp.code == code).first()

        if not otp or otp.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired otp code",
            )
        user = db.query(User).filter(User.id == otp.user_id).first()

        user.is_active = True

        db.commit()
        db.refresh(user)

        access_token, expiry = self.generate_access_token(db, user).values()

        user.last_login = datetime.now(timezone.utc)
        db.commit()
        db.refresh(user)

        response = {
            "access_token": access_token,
            "expiry_time": expiry,
            "user": UserResponseSchema(**jsonable_encoder(user)),
        }
        return response

    def create_otp_for_user(self, db: Session, user: User):
        otp = Otp(user_id=user.id)
        otp.generate_otp()

        db.add(otp)
        db.commit()
        db.refresh(otp)

        return otp.code

    def send_mail(self, receiver: str, code: int):
        msg = MIMEText(f"Use this otp code to verify your email account {code}")
        msg["Subject"] = "Email Verification"
        msg["From"] = SENDER
        msg["To"] = receiver

        try:
            with smtplib.SMTP(str(EMAIL_HOST), EMAIL_PORT, timeout=60) as server:
                server.starttls()
                server.login(SENDER, PASSWORD)
                server.sendmail(SENDER, receiver, msg.as_string())
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error sending email: {str(e)}"
            )

    def get_user_by_email(self, db: Session, email: str) -> User:
        user = db.query(User).filter(User.email == email).first()

        return user

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

    def create_user(
        self,
        db: Session,
        schema: UserCreateSchema,
        background_tasks: BackgroundTasks = BackgroundTasks(),
    ):

        try:

            user_exist = self.user_exist(
                db=db, email=schema.email, username=schema.username
            )

            # Password hashing

            hashed_password = self.hash_password(schema.password)
            schema.password = hashed_password
            user = User(**schema.model_dump())

            db.add(user)
            db.commit()
            db.refresh(user)

            try:
                # Send mail
                otp = self.create_otp_for_user(db, user)
                background_tasks.add_task(self.send_mail, user.email, otp)

            except Exception as email_error:
                db.rollback()
                raise email_error

            response = {
                "user": UserResponseSchema(**jsonable_encoder(user)),
            }

        except Exception as e:
            # If there's any other error, rollback and raise error
            db.rollback()
            raise e

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

        if user.is_active == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user, please verify your email",
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

    def blacklist_token(self, db: Session, user: User):

        access_token = (
            db.query(AccessToken).filter(AccessToken.user_id == user.id).first()
        )

        access_token.blacklisted = True

        db.commit()
        db.refresh(access_token)

    def get_current_user(
        self,
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
    ):

        credential_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            email: str = payload.get("email")

            if not email:
                raise credential_exception

        except jwt.InvalidTokenError:
            raise credential_exception

        access_token = db.query(AccessToken).filter(AccessToken.token == token).first()

        if access_token and access_token.blacklisted:
            raise credential_exception

        user = self.get_user_by_email(db, email)

        if not user:
            raise credential_exception

        if user.is_active == False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive User"
            )

        return user

    # User management functions

    def update(self, db: Session, schema: UserUpdateSchema, user: User, user_id: UUID4):
        schema_dict = schema.model_dump(exclude_unset=True)

        if user.id != user_id and user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have the permission to update this profile",
            )

        for key, value in schema_dict.items():
            if key == "role" and user.role != "admin":
                continue
            setattr(user, key, value)

        db.commit()
        db.refresh(user)

        return UserResponseSchema(**jsonable_encoder(user))

    def delete_user(self, db: Session, user_id: UUID4, user: User):
        if user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have the permission to delete this user",
            )

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
            )
        db.delete(user)
        db.commit()


user_service = UserService()
