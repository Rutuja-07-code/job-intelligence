from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..models import Job, Company

def create_job(db: Session,job: Job
):
    try:
        db.add(job)
        db.commit()
        db.refresh(job)

    except IntegrityError:
        db.rollback()
        raise

    return job

def get_company_jobs(
    db: Session,
    company_id: int,
    user_id: int
):
    jobs = (
        db.query(Job)
        .filter(
            Job.company_id == company_id,
            Job.user_id == user_id
        )
        .all()
    )

    return jobs
    
def get_jobs_with_company(db: Session, user_id: int):

    results = (
        db.query(Job, Company)
        .join(Company, Job.company_id == Company.id)
        .filter(Job.user_id == user_id)
        .all()
    )

    return [
        {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "company_id": company.id,
            "company_name": company.name
        }
        for job, company in results
    ]