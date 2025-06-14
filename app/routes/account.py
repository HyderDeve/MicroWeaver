from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.account import AccountCreate, Account
from app.services.account import AccountService

router = APIRouter()

@router.post("/", response_model=Account)
async def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    """Create a new account."""
    try:
        account_service = AccountService(db)
        return await account_service.create_account(account)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create account")

@router.get("/{account_id}", response_model=Account)
async def get_account(account_id: int, db: Session = Depends(get_db)):
    """Get account details by ID."""
    try:
        account_service = AccountService(db)
        account = await account_service.get_account(account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve account")