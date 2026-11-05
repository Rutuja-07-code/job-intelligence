from ..models import JobRequirement
from .company_service import get_or_create_company
from .skill_extraction_service import extract_skills

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

def import_jobs(jobs: list, db: Session, user_id: int):

    imported = 0
    skipped = 0

    for job_data in jobs:

        # 1. Extract basic job information
        title = job_data.get("title")
        description = job_data.get("description") or ""

        company_data = job_data.get("company") or {}
        location_data = job_data.get("location") or {}

        company_name = company_data.get("display_name")
        company_website = company_data.get("website")

        location = location_data.get("display_name")
        # 2. Skip jobs with missing information
        if not title or not company_name:
            skipped += 1
            continue

        # 3. Find or create company
        company = get_or_create_company(
            db,
            company_name,
            company_website
        )
        # 4. Check whether this job already exists
        existing_job = db.query(Job).filter(
            Job.company_id == company.id,
            Job.title == title
        ).first()

        if existing_job:
            skipped += 1
            continue

        # 5. Create job
        new_job = Job(
            user_id=user_id,
            company_id=company.id,
            title=title,
            description=description,
            location=location
        )

        try:
            db.add(new_job)
            db.flush()

            # 6. Extract skills
            skills = extract_skills(description)

            # 7. Save skills as job requirements
            for skill in skills:
                requirement = JobRequirement(
                    job_id=new_job.id,
                    skill_name=skill
                )
                db.add(requirement)

            db.commit()
            imported += 1

        except Exception:
            db.rollback()
            raise

    return {
        "imported": imported,
        "skipped": skipped
    }