from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.portofolio_model import PortofolioAccount
from app.db.models.transaction_model import Transaction
from app.db.models.mutation_model import Mutation

class OverbookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_account_by_number(self, account_number: str) -> PortofolioAccount | None:
        result = await self.db.execute(select(PortofolioAccount).where(PortofolioAccount.account_number == account_number))
        return result.scalars().first()

    def add_transaction(self, transaction: Transaction):
        self.db.add(transaction)

    def add_mutation(self, mutation: Mutation):
        self.db.add(mutation)

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()
    
    async def refresh(self, instance):
        await self.db.refresh(instance)
