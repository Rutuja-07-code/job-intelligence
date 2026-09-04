from sqlalchemy.orm import Session

from ..models import Company


def get_all_companies(db: Session):
    return db.query(Company).all()

def get_company_by_id(
    db: Session,
    company_id: int
    ):
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )
    return company

def create_company(db: Session, company:Company):
    db.add(company)
    db.commit()
    db.refresh(company)

    return company

def update_company(
    db: Session,
    company:Company
):

    try:
        db.commit()
        db.refresh(company)
    except Exception:
        db.rollback()
        raise
    return company