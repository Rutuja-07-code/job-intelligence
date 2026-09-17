import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from sqlalchemy.engine import URL
import pytest
from app.models import User, Job

load_dotenv()

TEST_DATABASE_URL=URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USER_TEST"),
    password=os.getenv("DB_PASSWORD_TEST"),
    host="localhost",
    port=5432,
    database="job_intelligence_test",
)
engine = create_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
Base.metadata.create_all(bind=engine)

def get_test_db():
    db=TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
@pytest.fixture(autouse=True)
def clean_database():
    db = TestSessionLocal()
    db.query(Job).delete()
    db.query(User).delete()
    db.commit()

    yield
    db.query(Job).delete()
    db.query(User).delete()
    db.commit()
    db.close()