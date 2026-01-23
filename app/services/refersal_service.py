from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.refersal_schema import RefersalRequest
from app.repositories.refersal_repository import RefersalRepository
from app.db.models.mutation_model import Mutation, MutationType

async def refersal_service(db: AsyncSession, request: RefersalRequest):
    repo = RefersalRepository(db)

    # Validate Transaction
    transaction = await repo.get_transaction_by_id(request.transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Validate Account
    account = await repo.get_account_by_number(transaction.source_account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Source account not found")
    
    # Refund Balance
    account.balance += transaction.amount
    
    # Create Mutation
    mutation = Mutation(
        account_number=account.account_number,
        transaction_id=transaction.transaction_id,
        mutation_type=MutationType.Refersal,
        amount=transaction.amount,
        balance_after=account.balance
    )
    
    repo.add(mutation)
    
    try:
        await repo.commit()
        await repo.refresh(account)
    except Exception as e:
        await repo.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "message": "Reversal successful", 
        "transaction_id": transaction.transaction_id,
        "new_balance": account.balance
    }
