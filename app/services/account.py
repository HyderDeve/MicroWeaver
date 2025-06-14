from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime

from app.models.account import Account as AccountModel
from app.schemas.account import AccountCreate
from app.core.security import get_password_hash

class AccountService:
    def __init__(self, db: Session):
        self.db = db

    async def create_account(self, account_data: AccountCreate) -> AccountModel:
        """Create a new account."""
        # Check if email already exists
        if self.get_account_by_email(account_data.email):
            raise ValueError("Email already registered")

        # Create new account
        db_account = AccountModel(
            email=account_data.email,
            username=account_data.username,
            full_name=account_data.full_name,
            hashed_password=get_password_hash(account_data.password)
        )

        self.db.add(db_account)
        self.db.commit()
        self.db.refresh(db_account)

        return db_account

    async def get_account(self, account_id: int) -> Optional[AccountModel]:
        """Get account by ID."""
        return self.db.query(AccountModel).filter(AccountModel.id == account_id).first()

    def get_account_by_email(self, email: str) -> Optional[AccountModel]:
        """Get account by email."""
        return self.db.query(AccountModel).filter(AccountModel.email == email).first()