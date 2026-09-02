from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Job, Company
from ..schemas import (
    JobResponse,
    JobCreate,
    JobWithCompanyResponse
)

router = APIRouter(
    prefix="",
    tags=["Jobs"]
)

# create job
from ..services.job_service import create_job
@router.post(
    "/companies/{company_id}/jobs",
    response_model=JobResponse
)
def create_job_endpoint(
    company_id: int,
    job_data: JobCreate,
    db: Session = Depends(get_db)
):
    return create_job(company_id,job_data,db)

# get jobs
from ..services.job_service import get_company_jobs
@router.get(
    "/companies/{company_id}/jobs",
    response_model=list[JobResponse]
)
def get_company_jobs_endpoint(
    company_id: int,
    db: Session = Depends(get_db)
):
    return get_company_jobs(company_id,db)

#retrive comapany any info while also want info fro job
from ..services.job_service import get_jobs
@router.get("/jobs", response_model=list[JobWithCompanyResponse])
def get_jobs_endpoint(db: Session = Depends(get_db)):
    return get_jobs(db)
