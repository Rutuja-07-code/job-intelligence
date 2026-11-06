from app.services.skill_extraction_service import extract_skills


def test_extracts_skills_without_matching_java_inside_javascript():
    description = (
        "We need a JavaScript developer with React.js, PostgreSQL, "
        "Docker and Git experience."
    )

    assert extract_skills(description) == [
        "JavaScript",
        "React",
        "PostgreSQL",
        "Docker",
        "Git",
    ]


def test_returns_empty_list_for_empty_description():
    assert extract_skills("") == []
    assert extract_skills(None) == []
