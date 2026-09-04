from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Company
from ..schemas import CompanyCreate, CompanyUpdate
from ..repositories.company_repository import (
    get_all_companies, 
    get_company_by_id,
    create_company as create_company_db,
    update_company as update_company_db
)

# get companies
def get_companies(db:Session):
    return get_all_companies(db)

#creat company
def create_company(db: Session, company_data: CompanyCreate):
    new_company = Company(
        name=company_data.name,
        website=company_data.website
    )

    return create_company_db(db, new_company)

#get company
def get_company(
    company_id: int,db: Session):
    company = get_company_by_id(db, company_id)
    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )
    return company

#updating
def update_company(
    company_id: int,
    company_data:CompanyUpdate,
    db: Session
):
    company = get_company_by_id(db, company_id)

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )
    company.name = company_data.name
    company.website = company_data.website
    return update_company_db(db, company)