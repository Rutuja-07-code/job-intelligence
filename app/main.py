from fastapi import FastAPI, Depends,HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import Company, Job
from .schemas import (
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
    JobCreate,
    JobResponse,
    JobWithCompanyResponse
)
app = FastAPI()


# create company
@app.post("/companies")
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    new_company = Company(
        name=company.name,
        website=company.website
    )

    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    return new_company
@app.get("/companies", response_model=list[CompanyResponse])
def get_companies(db:Session=Depends(get_db)):
    companies=db.query(Company).all()
    return companies

# getting specific row of specific id
@app.get("/companies/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db)
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
    return company

# updating
@app.put("/companies/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db)
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
# create jobs

@app.post(
    "/companies/{company_id}/jobs",
    response_model=JobResponse
)
def create_job(
    company_id: int,
    job_data: JobCreate,
    db: Session = Depends(get_db)
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

    new_job = Job(
        company_id=company_id,
        title=job_data.title,
        description=job_data.description
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job
# get jobs

@app.get(
    "/companies/{company_id}/jobs",
    response_model=list[JobResponse]
)
def get_company_jobs(
    company_id: int,
    db: Session = Depends(get_db)
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

    return company.jobs

#retrive comapany any info while also want info fro job
@app.get("/jobs", response_model=list[JobWithCompanyResponse])
def get_jobs(db: Session = Depends(get_db)):

    results = (
        db.query(Job, Company)
        .join(Company, Job.company_id == Company.id)
        .all()
    )

    return [
        {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "company_id": company.id,
            "company_name": company.name
        }
        for job, company in results
    ]