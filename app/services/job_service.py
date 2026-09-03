from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Job , Company
from ..schemas import JobCreate

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

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

#get job
def get_company_jobs(
    company_id: int,
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

    return (
        db.query(Job)
        .filter(Job.company_id == company_id)
        .all()
    )

#retrive comapany any info while also want info fro job
def get_jobs(db: Session):

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