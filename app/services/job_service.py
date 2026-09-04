from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Job , Company
from ..schemas import JobCreate
from ..repositories.job_repository import (
    create_job as create_job_db,
    get_company_jobs as find_company_jobs,
    get_jobs_with_company
)

def create_job(
    company_id: int,
    job_data: JobCreate,
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

    new_job = Job(
        company_id=company_id,
        title=job_data.title,
        description=job_data.description
    )
    return create_job_db(db, new_job)

#get job
def get_company_jobs(
    company_id: int,
    db: Session
):
    jobs=find_company_jobs(db, company_id)

    if jobs is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return jobs

#retrive comapany any info while also want info fro job
def get_jobs(db: Session):
    return get_jobs_with_company(db)