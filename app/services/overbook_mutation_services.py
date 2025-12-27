# app/services/overbook_mutation_services.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.transaction_model import Transaction, TransactionType, TransactionBank
from app.db.models.mutation_model import Mutation, MutationType
from app.db.models.portofolio_model import PortofolioAccount
from app.schemas.overbook_mutation_schema import OverbookMutationRequest
from app.repositories.overbook_repository import OverbookRepository
from datetime import datetime
import time
from decimal import Decimal

async def post_overbook_transaction_service(db: AsyncSession, request: OverbookMutationRequest):
    repository = OverbookRepository(db)

    # Validate Source Account
    source_account = await repository.get_account_by_number(request.source_account_number)

    if not source_account:
        raise HTTPException(status_code=404, detail="Source account not found")

    # Validate Target Account
    target_account = await repository.get_account_by_number(request.target_account_number)

    if not target_account:
        raise HTTPException(status_code=404, detail="Target account not found")

    # Check Balance
    amount_decimal = Decimal(str(request.amount))
    if source_account.balance < amount_decimal:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    
    # Check Transaction Type
    if request.transaction_type != "TrfOvrbok":
        raise HTTPException(status_code=400, detail="Invalid transaction type for overbook")

    
    # Determine Transaction ID
    transaction_id = request.transaction_id
    if transaction_id is None:
        raise HTTPException(status_code=400, detail="Empty id transaction")
    
    # Create Transaction
    try:
        transaction_type_enum = TransactionType(request.transaction_type)
        transaction_bank_enum = TransactionBank(request.transaction_bank)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid transaction type or bank")

    new_transaction = Transaction(
        transaction_id=transaction_id,
        transaction_type=transaction_type_enum,
        transaction_bank=transaction_bank_enum,
        bank_reference=request.bank_reference,
        source_account_number=request.source_account_number,
        target_account_number=request.target_account_number,
        amount=amount_decimal,
        currency_code=request.currency_code,
        description=request.description,
        transaction_date=request.transaction_date or datetime.now()
    )

    repository.add_transaction(new_transaction)
    
    # Update Balances
    source_account.balance -= amount_decimal
    target_account.balance += amount_decimal
    
    # Create Mutations
    # Source (Kredit)
    source_mutation = Mutation(
        account_number=source_account.account_number,
        transaction_id=transaction_id,
        mutation_type=MutationType.Kredit,
        amount=amount_decimal,
        balance_after=source_account.balance
    )
    
    # Target (Debit)
    target_mutation = Mutation(
        account_number=target_account.account_number,
        transaction_id=transaction_id,
        mutation_type=MutationType.Debit,
        amount=amount_decimal,
        balance_after=target_account.balance
    )
    
    repository.add_mutation(source_mutation)
    repository.add_mutation(target_mutation)
    
    try:
        await repository.commit()
        await repository.refresh(new_transaction)
    except Exception as e:
        await repository.rollback()
        raise HTTPException(status_code=500, detail=str(e))
        
    return new_transaction
