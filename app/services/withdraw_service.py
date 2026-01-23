from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.withdraw_schema import WithdrawRequest
from app.repositories.withdraw_repository import WithdrawRepository
from app.db.models.mutation_model import Mutation, MutationType
from datetime import datetime

async def withdraw_service(db: AsyncSession, request: WithdrawRequest):
    repo = WithdrawRepository(db)

    # Fetch the account
    account = await repo.get_account_by_number(request.account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Check for sufficient balance
    if account.balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Deduct the amount from the account balance
    account.balance -= request.amount
    repo.add(account)

    # Create a mutation record
    mutation = Mutation(
        account_number=account.account_number,
        transaction_id=None,
        mutation_type=MutationType.TarikTunai,
        amount=request.amount,
        balance_after=account.balance
    )
    repo.add(mutation)

    try:
        await repo.commit()
        await repo.refresh(account)
        # await repo.refresh(mutation)
    except Exception as e:
        await repo.rollback()
        raise HTTPException(status_code=500, detail="Failed to process withdrawal") from e

    return {
        "account_number": account.account_number,
        "withdrawn_amount": request.amount,
        "new_balance": account.balance
    }