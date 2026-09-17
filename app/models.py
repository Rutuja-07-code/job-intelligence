from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


from .database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    website = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())

    #build relationship
    jobs = relationship("Job", back_populates="company")

class Job(Base):
    __tablename__ = "jobs"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "title",
            name="unique_company_job_title"
        ),
        Index(
        "idx_jobs_company_id",
        "company_id"
        ),

    )

    id = Column(Integer, primary_key=True)
    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
)   
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    title = Column(String(150), nullable=False)
    description = Column(Text)
    location = Column(String(150))
    created_at = Column(DateTime, server_default=func.now())

    company = relationship("Company", back_populates="jobs")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())