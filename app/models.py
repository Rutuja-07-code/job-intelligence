from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
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

    id = Column(Integer, primary_key=True)
    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )
    title = Column(String(150), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

    #build relationship
    company = relationship("Company", back_populates="jobs")
