
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..dependencies import get_current_user
from ..schemas import ProfileCreate, ProfileResponse, SkillCreate
from ..models import Profile, Skill

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.post("", response_model=ProfileResponse)
def create_profile(
    profile_data: ProfileCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    existing_profile = (
        db.query(Profile)
        .filter(Profile.user_id == user_id)
        .first()
    )

    if existing_profile:
        raise HTTPException(
            status_code=409,
            detail="Profile already exists"
        )

    new_profile = Profile(
        user_id=user_id,
        full_name=profile_data.full_name
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile



@router.get("", response_model=ProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    profile = (
        db.query(Profile)
        .filter(Profile.user_id == user_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile


@router.post("/skills")
def add_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    profile = (
        db.query(Profile)
        .filter(Profile.user_id == user_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Create your profile first"
        )

    existing_skill = (
        db.query(Skill)
        .filter(
            Skill.profile_id == profile.id,
            Skill.name == skill_data.name
        )
        .first()
    )

    if existing_skill:
        raise HTTPException(
            status_code=409,
            detail="Skill already exists"
        )

    new_skill = Skill(
        profile_id=profile.id,
        name=skill_data.name
    )

    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)

    return new_skill


@router.get("/skills")
def get_skills(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    profile = (
        db.query(Profile)
        .filter(Profile.user_id == user_id)
        .first()
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    skills = (
        db.query(Skill)
        .filter(Skill.profile_id == profile.id)
        .all()
    )

    return skills
