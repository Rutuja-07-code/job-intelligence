import requests
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models import Job, Company, JobRequirement
from ..schemas import JobCreate
from ..repositories.job_repository import (
    create_job as create_job_db,
    get_company_jobs as find_company_jobs,
    get_jobs_with_company
)
from .adzuna_service import fetch_jobs
from .company_service import get_or_create_company
from .skill_extraction_service import extract_skills


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
            detail="You already saved a job with this title for this company"
        )


def get_company_jobs(
    company_id: int,
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

    return find_company_jobs(db, company_id, user_id)


def get_jobs(db: Session, user_id: int):
    return get_jobs_with_company(db, user_id)


def import_jobs(jobs: list, db: Session, user_id: int):
    imported = 0
    skipped = 0

    for job_data in jobs:
        title = (job_data.get("title") or "").strip()
        description = job_data.get("description") or ""

        company_data = job_data.get("company") or {}
        location_data = job_data.get("location") or {}

        company_name = (company_data.get("display_name") or "").strip()
        company_website = company_data.get("website")
        location = location_data.get("display_name")

        if not title or not company_name:
            skipped += 1
            continue

        company = get_or_create_company(
            db,
            company_name,
            company_website
        )

        if company is None:
            skipped += 1
            continue

        existing_job = db.query(Job).filter(
            Job.user_id == user_id,
            Job.company_id == company.id,
            Job.title == title
        ).first()

        if existing_job:
            skipped += 1
            continue

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

            for skill in extract_skills(description):
                db.add(
                    JobRequirement(
                        job_id=new_job.id,
                        skill_name=skill
                    )
                )

            db.commit()
            imported += 1

        except Exception:
            db.rollback()
            raise

    return {
        "imported": imported,
        "skipped": skipped
    }


def import_adzuna_jobs(
    keyword: str,
    location: str,
    results_per_page: int,
    db: Session,
    user_id: int
):
    try:
        jobs = fetch_jobs(
            keyword=keyword,
            location=location,
            results_per_page=results_per_page
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=503,
            detail="Adzuna API credentials are not configured"
        ) from exc
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to fetch jobs from Adzuna"
        ) from exc

    result = import_jobs(jobs, db, user_id)

    return {
        "fetched": len(jobs),
        **result
    }
