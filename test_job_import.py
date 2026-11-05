from app.database import SessionLocal
from app.services.adzuna_service import fetch_jobs
from app.services.job_service import import_jobs

db = SessionLocal()

try:
    jobs = fetch_jobs(
        keyword="Python Developer",
        location="Pune",
        results_per_page=20
    )

    print("Jobs received:", len(jobs))

    for job in jobs:
        print(
            "Title:", job.get("title"),
            "Company:", job.get("company"),
            "Location:", job.get("location")
        )

    result = import_jobs(
        jobs=jobs,
        db=db,
        user_id=5
    )

    print("Import result:", result)

finally:
    db.close()