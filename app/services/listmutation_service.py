from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.mutation_model import Mutation, MutationType
from app.schemas.listmutation_schema import ListMutation
from app.repositories.mutation_repository import MutationRepository
from datetime import datetime
from app.utils.request_middleware import send_to_middleware

async def get_list_mutation_service(db: AsyncSession, request: ListMutation):
    repository = MutationRepository(db)

    # Validate account existence
    account = await repository.get_account_by_number(request.account_number)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Parse dates
    try:
        start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
        end_date = end_date.replace(hour=23, minute=59, second=59)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Fetch mutations from the database
    mutations = await repository.get_mutations_by_account_and_date_range(
        request.account_number, start_date, end_date
    )
    print(f"DEBUG: account number: {request.account_number}, start_date: {start_date}, end_date: {end_date}")
    # If no mutations found, return empty list
    print(f"DEBUG: Found {len(mutations)} mutations from DB")
    if not mutations:
        print("DEBUG: No mutations found, returning empty list")
        return []

    # Prepare response data
    print(f"DEBUG: Processing {len(mutations)} mutations")
    mutation_list = []
    for mutation in mutations:
        # Determine related account based on mutation type
        related_account_number = None
        description = None
        
        if mutation.transaction:
            description = mutation.transaction.description
            if mutation.mutation_type.value == "Debit":
                related_account_number = mutation.transaction.target_account_number
            elif mutation.mutation_type.value == "Kredit":
                related_account_number = mutation.transaction.source_account_number

        mutation_list.append({
            "transaction_id": mutation.transaction_id,
            "mutation_type": mutation.mutation_type.value,
            "amount": float(mutation.amount),
            "balance_after": float(mutation.balance_after),
            "timestamp": mutation.created_at.isoformat(),
            "description": description,
            "related_account_number": related_account_number
        })
    
    print(mutation_list)
    return mutation_list