from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Company
from ..schemas import CompanyCreate, CompanyUpdate

#creat company
def create_company(db: Session, company_data: CompanyCreate):
    new_company = Company(
        name=company_data.name,
        website=company_data.website
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company

# get companies
def get_companies(db:Session):
    companies=db.query(Company).all()
    return companies

#get company
def get_company(
    company_id: int,db: Session):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

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
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )
    try:
        company.name = company_data.name
        company.website = company_data.website

        db.commit()
        db.refresh(company)
    except Exception:
        db.rollback()
        raise
    return company