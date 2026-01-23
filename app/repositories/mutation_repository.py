from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload
from app.db.models.portofolio_model import PortofolioAccount
from app.db.models.transaction_model import Transaction
from app.db.models.mutation_model import Mutation

class MutationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_account_by_number(self, account_number: str) -> PortofolioAccount | None:
        result = await self.db.execute(select(PortofolioAccount).where(PortofolioAccount.account_number == account_number))
        return result.scalars().first()

    def add_transaction(self, transaction: Transaction):
        self.db.add(transaction)

    def add_mutation(self, mutation: Mutation):
        self.db.add(mutation)

    async def update_balance(self, account_number: str, new_balance):
        await self.db.execute(
            update(PortofolioAccount)
            .where(PortofolioAccount.account_number == account_number)
            .values(balance=new_balance)
        )

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()
    
    async def refresh(self, instance):
        await self.db.refresh(instance)

    async def get_mutations_by_account_and_date_range(self, account_number: str, start_date, end_date):
        result = await self.db.execute(
            select(Mutation)
            .options(selectinload(Mutation.transaction))
            .where(
                Mutation.account_number == account_number,
                Mutation.created_at >= start_date,
                Mutation.created_at <= end_date
            )
            .order_by(Mutation.created_at.desc())
        )
        return result.scalars().all()
