from sqlalchemy.orm import Session
from src.main.api.db.models.user_table import User


class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return (
            db.query(User)
            .filter_by(username=username)
            .filter(User.deleted_at.is_(None))   # только активные; обязательно из-за soft-delete
            .first()
        )

    @staticmethod
    def create_user(db: Session, username: str, password: str, role: str) -> User:
        user = User(
            username=username,
            password=password,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
