from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.portofolio_repository import PortofolioRepository
from app.schemas.create_porto_schema import RegisterRequest
from app.db.models.portofolio_model import PortofolioAccount
from app.db.models.customer_model import Customer

async def create_portofolio_service(db: AsyncSession, data: RegisterRequest):
    repo = PortofolioRepository(db)
    
    try:
        # Check if customer already exists
        existing_customer = await repo.get_customer_by_nik(data.nik)
        if existing_customer:
            raise HTTPException(status_code=400, detail="Customer with this NIK already exists")

        # Check if account number already exists
        existing_account = await repo.get_portofolio_by_account_number(data.account_number)
        if existing_account:
            raise HTTPException(status_code=400, detail="Account number already exists")

        # 1. Create Customer
        new_customer = Customer(
            full_name=data.full_name,
            birth_date=data.birth_date,
            address=data.address,
            NIK=data.nik,
            phone_number=data.phone_number,
            email=data.email
        )
        created_customer = await repo.create_customer(new_customer)
        
        # 2. Create Portofolio linked to Customer
        new_portofolio = PortofolioAccount(
            account_number=data.account_number,
            customer_id=created_customer.customer_id
        )
        await repo.create_portofolio(new_portofolio)
        
        # Capture values before commit expires the instances
        cid = created_customer.customer_id
        acc_num = new_portofolio.account_number

        await db.commit()
        
        return {
            "message": "Portofolio created successfully",
            "customer_id": cid,
            "account_number": acc_num
        }
        
    except Exception as e:
        await db.rollback()
        raise e


