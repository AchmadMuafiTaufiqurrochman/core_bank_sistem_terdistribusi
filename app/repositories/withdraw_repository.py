from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.portofolio_model import PortofolioAccount
from app.db.models.customer_model import Customer

class WithdrawRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_account_by_number(self, account_number: str) -> PortofolioAccount | None:
        result = await self.db.execute(select(PortofolioAccount).where(PortofolioAccount.account_number == account_number))
        return result.scalars().first()

    async def get_customer_by_id(self, customer_id: int) -> Customer | None:
        result = await self.db.execute(select(Customer).where(Customer.id == customer_id))
        return result.scalars().first()

    def add(self, instance):
        self.db.add(instance)

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()
    
    async def refresh(self, instance):
        await self.db.refresh(instance)