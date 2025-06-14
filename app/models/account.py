from app.models.base import Base, TimestampMixin, UUIDMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class Account(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "accounts"

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
