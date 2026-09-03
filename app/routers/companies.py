from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Company
from ..schemas import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse
)

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)


# create company
from ..services.company_service import create_company
@router.post("/", response_model=CompanyResponse)
def create_company_endpoint(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    return create_company(db, company)

#get company
from ..services.company_service import get_companies
@router.get("/", response_model=list[CompanyResponse])
def get_companies_endpoint(db:Session=Depends(get_db)):
    return get_companies(db)

# getting specific row of specific id
from ..services.company_service import get_company
@router.get("/{company_id}", response_model=CompanyResponse)
def get_company_endpoint(
    company_id: int,
    db: Session = Depends(get_db)
):
    return get_company(company_id,db)

# updating
from ..services.company_service import update_company
@router.put("/{company_id}", response_model=CompanyResponse)
def update_company_endpoint(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db)
):
    return update_company(company_id,company_data,db)