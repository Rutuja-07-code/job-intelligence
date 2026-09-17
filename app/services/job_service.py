from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Job , Company
from ..schemas import JobCreate
from ..repositories.job_repository import (
    create_job as create_job_db,
    get_company_jobs as find_company_jobs,
    get_jobs_with_company
)
from sqlalchemy.exc import IntegrityError

def create_job(
    company_id: int,
    job_data: JobCreate,
    db: Session,
    user_id: int
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
        user_id=user_id,
        company_id=company_id,
        title=job_data.title,
        description=job_data.description,
        location=job_data.location

    )
    try:
        return create_job_db(db, new_job)

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="A job with this title already exists for this company"
        )
#get job
def get_company_jobs(
    company_id: int,
    db: Session,
    user_id: int
):
    jobs=find_company_jobs(db, company_id, user_id)

    if jobs is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    return jobs

#retrive comapany any info while also want info fro job
def get_jobs(db: Session, user_id: int):
    return get_jobs_with_company(db, user_id)