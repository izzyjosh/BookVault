from fastapi import Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.v1.utils.dependencies import get_db
from api.v1.models.user import User
from api.v1.services.user import user_service
from api.v1.schemas.user import UserResponseSchema


class AdminService:
    def check_user_role(self, user: User, required_role: str):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this endpoint",
            )
        return UserResponseSchema(**jsonable_encoder(user))

    def update_role(
        self,
        user: User = Depends(user_service.get_current_user),
    ):
        response = self.check_user_role(user, "admin")
        return response

    def fetch_users(self, db: Session):
        users = db.query(User).all()

        return jsonable_encoder(users)


admin_service = AdminService()
