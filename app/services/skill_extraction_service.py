import re


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
    description = (description or "").casefold()

    extracted_skills = []

    for skill, keywords in SKILL_DICTIONARY.items():
        for keyword in keywords:
            pattern = rf"(?<!\w){re.escape(keyword.casefold())}(?!\w)"
            if re.search(pattern, description):
                extracted_skills.append(skill)
                break

    return extracted_skills
