
SKILL_DICTIONARY = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js"],
    "React": ["react", "react.js"],
    "FastAPI": ["fastapi"],
    "Django": ["django"],
    "PostgreSQL": ["postgresql", "postgres"],
    "MySQL": ["mysql"],
    "MongoDB": ["mongodb"],
    "Docker": ["docker"],
    "Git": ["git"],
    "AWS": ["aws", "amazon web services"],
    "REST API": ["rest api", "rest apis"]
}


def extract_skills(description: str) -> list[str]:
    description = description.casefold()

    extracted_skills = []

    for skill, keywords in SKILL_DICTIONARY.items():
        for keyword in keywords:
            if keyword in description:
                extracted_skills.append(skill)
                break

    return extracted_skills

# from app.services.skill_extraction_service import extract_skills

description = """
We need a Python developer with experience in FastAPI,
PostgreSQL, REST APIs and Git.
Knowledge of Docker is preferred.
"""

skills = extract_skills(description)

print("Extracted skills:", skills)
