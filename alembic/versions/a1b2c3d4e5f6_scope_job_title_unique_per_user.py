"""scope job title uniqueness to each user

Revision ID: a1b2c3d4e5f6
Revises: 452c2ad352d1
Create Date: 2026-11-06

"""
from typing import Sequence, Union

from alembic import op


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "452c2ad352d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "unique_company_job_title",
        "jobs",
        type_="unique"
    )
    op.create_unique_constraint(
        "unique_user_company_job_title",
        "jobs",
        ["user_id", "company_id", "title"]
    )


def downgrade() -> None:
    op.drop_constraint(
        "unique_user_company_job_title",
        "jobs",
        type_="unique"
    )
    op.create_unique_constraint(
        "unique_company_job_title",
        "jobs",
        ["company_id", "title"]
    )
