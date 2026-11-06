from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..models import Job, JobRequirement
from ..schemas import (
    JobResponse,
    JobCreate,
    JobWithCompanyResponse,
    JobRequirementCreate,
    JobRequirementResponse,
    JobRecommendationResponse,
    JobImportRequest,
    JobImportResponse
)
from ..services.job_service import (
    create_job,
    get_company_jobs,
    get_jobs,
    import_adzuna_jobs
)
from ..services.recommendation_service import get_job_recommendations


router = APIRouter(
    prefix="",
    tags=["Jobs"]
)


@router.post(
    "/companies/{company_id}/jobs",
    response_model=JobResponse
)
def create_job_endpoint(
    company_id: int,
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return create_job(company_id, job_data, db, current_user)


@router.get(
    "/companies/{company_id}/jobs",
    response_model=list[JobResponse]
)
def get_company_jobs_endpoint(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return get_company_jobs(company_id, db, current_user)


@router.post(
    "/jobs/import",
    response_model=JobImportResponse
)
def import_adzuna_jobs_endpoint(
    import_data: JobImportRequest,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return import_adzuna_jobs(
        keyword=import_data.keyword,
        location=import_data.location,
        results_per_page=import_data.results_per_page,
        db=db,
        user_id=current_user
    )


@router.get(
    "/jobs",
    response_model=list[JobWithCompanyResponse]
)
def get_jobs_endpoint(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return get_jobs(db, current_user)


@router.post(
    "/{job_id}/requirements",
    response_model=JobRequirementResponse,
    status_code=201
)
def add_job_requirement(
    job_id: int,
    requirement_data: JobRequirementCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == user_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    existing_requirement = db.query(JobRequirement).filter(
        JobRequirement.job_id == job_id,
        JobRequirement.skill_name == requirement_data.skill_name
    ).first()

    if existing_requirement:
        raise HTTPException(
            status_code=409,
            detail="This skill is already required for this job"
        )

    new_requirement = JobRequirement(
        job_id=job_id,
        skill_name=requirement_data.skill_name
    )

    db.add(new_requirement)
    db.commit()
    db.refresh(new_requirement)

    return new_requirement


@router.get(
    "/jobs/recommendations",
    response_model=list[JobRecommendationResponse]
)
def get_job_recommendations_endpoint(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return get_job_recommendations(db, current_user)
