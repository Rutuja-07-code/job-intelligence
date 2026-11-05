from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Job, Company, JobRequirement
from ..schemas import (
    JobResponse,
    JobCreate,
    JobWithCompanyResponse,
    JobRequirementCreate, 
    JobRequirementResponse,
    JobRecommendationResponse
)
from ..services.recommendation_service import get_job_recommendations
from ..dependencies import get_current_user

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
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return create_job(company_id,job_data,db, current_user)

# get jobs
from ..services.job_service import get_company_jobs
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

#retrive comapany any info while also want info fro job
from ..services.job_service import get_jobs
@router.get("/jobs", response_model=list[JobWithCompanyResponse])
def get_jobs_endpoint(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)):
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
    # Find the job owned by the logged-in user
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == user_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Check whether this skill is already required
    existing_requirement = db.query(JobRequirement).filter(
        JobRequirement.job_id == job_id,
        JobRequirement.skill_name == requirement_data.skill_name
    ).first()

    if existing_requirement:
        raise HTTPException(
            status_code=409,
            detail="This skill is already required for this job"
        )

    # Create the requirement
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