from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Profile, Skill, Job


def get_job_recommendations(db: Session, user_id: int):

    # 1. Get user's profile
    profile = db.query(Profile).filter(
        Profile.user_id == user_id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="User profile not found"
        )

    # 2. Get user's skills
    user_skills = db.query(Skill).filter(
        Skill.profile_id == profile.id
    ).all()

    if not user_skills:
        raise HTTPException(
            status_code=400,
            detail="Please add skills to your profile first"
        )

    # Normalize skills for case-insensitive comparison
    user_skill_map = {
        skill.name.strip().casefold(): skill.name
        for skill in user_skills
    }

    # 3. Get jobs belonging to this user
    jobs = db.query(Job).filter(
        Job.user_id == user_id
    ).all()

    recommendations = []

    # 4. Compare user skills with each job
    for job in jobs:

        required_skills = [
            requirement.skill_name
            for requirement in job.requirements
        ]

        required_skill_map = {
            skill.strip().casefold(): skill
            for skill in required_skills
        }

        matched_skills = [
            user_skill_map[skill]
            for skill in required_skill_map
            if skill in user_skill_map
        ]

        missing_skills = [
            skill
            for skill in required_skill_map.values()
            if skill.casefold() not in user_skill_map
        ]

        total_required = len(required_skill_map)
        total_matched = len(matched_skills)

        # 5. Calculate matching percentage
        score = (
            (total_matched / total_required) * 100
            if total_required > 0
            else 0
        )

        # 6. Store recommendation
        recommendations.append({
            "job_id": job.id,
            "job_title": job.title,
            "company_name": job.company.name,
            "location": job.location,
            "match_score": round(score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        })

    # 7. Rank jobs from highest score to lowest
    recommendations.sort(
        key=lambda item: item["match_score"],
        reverse=True
    )

    return recommendations