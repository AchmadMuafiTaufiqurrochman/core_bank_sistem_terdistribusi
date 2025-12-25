from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.portofolio_model import PortofolioAccount
from app.db.models.customer_model import Customer

class PortofolioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_customer_by_nik(self, nik: str) -> Customer | None:
        result = await self.db.execute(select(Customer).where(Customer.NIK == nik))
        return result.scalars().first()

    async def get_portofolio_by_account_number(self, account_number: str) -> PortofolioAccount | None:
        result = await self.db.execute(select(PortofolioAccount).where(PortofolioAccount.account_number == account_number))
        return result.scalars().first()

    async def create_customer(self, customer: Customer) -> Customer:
        self.db.add(customer)
        await self.db.flush()
        return customer

    async def create_portofolio(self, portofolio: PortofolioAccount) -> PortofolioAccount:
        self.db.add(portofolio)
        await self.db.flush()
        return portofolio


