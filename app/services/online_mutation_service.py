from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.transaction_model import Transaction, TransactionType, TransactionBank
from app.db.models.mutation_model import Mutation, MutationType
from app.schemas.online_mutation_schema import OnlineMutationRequest
from app.repositories.mutation_repository import MutationRepository
from app.utils.request_middleware import send_to_middleware
from decimal import Decimal
import logging

# Setup logger
logger = logging.getLogger(__name__)

async def post_online_transaction_service(db: AsyncSession, request: OnlineMutationRequest):
    repository = MutationRepository(db)

    # 1. Validate Source Account
    source_account = await repository.get_account_by_number(request.source_account_number)
    if not source_account:
        raise HTTPException(status_code=404, detail="Source account not found")

    # 2. Check Balance
    amount_decimal = Decimal(str(request.amount))
    if source_account.balance < amount_decimal:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # 3. Create Transaction Record (Initial State)
    # Note: Ideally we should have a status field (PENDING), but using existing schema.
    transaction = Transaction(
        transaction_id=request.transaction_id,
        transaction_type=TransactionType.TrfOnln,
        transaction_bank=TransactionBank.Eksternal,
        source_account_number=request.source_account_number,
        target_account_number=request.target_account_number,
        amount=amount_decimal,
        description=request.description,
        currency_code=request.currency_code
    )
    repository.add_transaction(transaction)

    # 4. Deduct Balance (Debit Mutation)
    new_balance = source_account.balance - amount_decimal
    await repository.update_balance(request.source_account_number, new_balance)
    
    mutation = Mutation(
        account_number=request.source_account_number,
        transaction_id=request.transaction_id,
        mutation_type=MutationType.Debit,
        amount=amount_decimal,
        balance_after=new_balance
    )
    repository.add_mutation(mutation)

    # 5. Commit to persist the deduction
    try:
        await repository.commit()
    except Exception as e:
        await repository.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    # 6. Call Middleware (External System)
    try:
        # Prepare payload
        payload = request.model_dump(mode='json')
        
        # Send to middleware
        await send_to_middleware(payload)

        return {
            "status": "success",
            "message": "Online transaction successful",
            "transaction_id": request.transaction_id,
            "balance_after": new_balance
        }

    except Exception as e:
        logger.error(f"Middleware error: {e}")
        
        await repository.refresh(source_account)
        
        new_balance = source_account.balance + amount_decimal
        await repository.update_balance(request.source_account_number, new_balance)
        
        reversal_mutation = Mutation(
            account_number=request.source_account_number,
            transaction_id=request.transaction_id,
            mutation_type=MutationType.Kredit,
            amount=amount_decimal,
            balance_after=new_balance
        )
        repository.add_mutation(reversal_mutation)
        
        await repository.commit()
        
        return {
            "status": "failed", 
            "message": "Transaction failed at middleware. Funds have been reversed.",
            "transaction_id": request.transaction_id,
            "balance_after": new_balance
        }
