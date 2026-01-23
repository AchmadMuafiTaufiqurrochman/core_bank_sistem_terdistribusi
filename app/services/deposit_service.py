from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.deposit_schema import DepositRequest
from app.repositories.deposit_repository import DepositRepository
from app.db.models.mutation_model import Mutation, MutationType
from datetime import datetime

async def deposit_service(db: AsyncSession, request: DepositRequest):
    repository = DepositRepository(db)
    
    account = await repository.get_account_by_number(request.account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Update balance
    account.balance += request.amount
    
    # Create Mutation record
    mutation = Mutation(
        account_number=account.account_number,
        transaction_id=None,
        mutation_type=MutationType.SetorTunai,
        amount=request.amount,
        balance_after=account.balance
    )
    repository.add(mutation)

    try:
        await repository.commit()
        await repository.refresh(account)
    except Exception as e:
        await repository.rollback()
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"message": "Deposit successful", "new_balance": account.balance, "account_number": account.account_number}
