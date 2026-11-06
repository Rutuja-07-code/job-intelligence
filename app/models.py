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
            "user_id",
            "company_id",
            "title",
            name="unique_user_company_job_title"
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
    requirements = relationship(
        "JobRequirement",
        back_populates="job",
        cascade="all, delete-orphan"
    )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    profile = relationship(
        "Profile",
        back_populates="user",
        uselist=False
    )

class Skill(Base):
    __tablename__ = "skills"

    __table_args__ = (
        UniqueConstraint(
            "profile_id",
            "name",
            name="unique_profile_skill"
        ),
    )

    id = Column(Integer, primary_key=True)

    profile_id = Column(
        Integer,
        ForeignKey("profiles.id"),
        nullable=False
    )

    name = Column(String(100), nullable=False)

    profile = relationship(
        "Profile",
        back_populates="skills"
    )


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True
    )
    created_at = Column(DateTime, server_default=func.now())

    full_name = Column(String(100), nullable=False)
    user = relationship("User", back_populates="profile")

    skills = relationship(
        "Skill",
        back_populates="profile",
        cascade="all, delete-orphan"
    )


class JobRequirement(Base):
    __tablename__ = "job_requirements"

    __table_args__ = (
        UniqueConstraint(
            "job_id",
            "skill_name",
            name="unique_job_skill_requirement"
        ),
    )

    id = Column(Integer, primary_key=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    skill_name = Column(String(100), nullable=False)

    job = relationship("Job", back_populates="requirements")
