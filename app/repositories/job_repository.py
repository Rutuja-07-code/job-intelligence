from sqlalchemy.orm import Session

from ..models import Job, Company

def create_job(db: Session,job: Job
):
    db.add(job)
    db.commit()
    db.refresh(job)

    return job

def get_company_jobs(
    db: Session,
    company_id: int
):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if company is None:
        None
    jobs = (
        db.query(Job)
        .filter(Job.company_id == company_id)
        .all())
    return jobs
    
def get_jobs_with_company(db: Session):

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