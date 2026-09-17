"""add user ownership to jobs

Revision ID: f3f238958c13
Revises: ecfad843f428
Create Date: 2026-09-09 14:30:54.056322

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3f238958c13'
down_revision: Union[str, Sequence[str], None] = 'ecfad843f428'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'jobs',
        sa.Column('user_id', sa.Integer(), nullable=True)
    )

    op.execute(
        "UPDATE jobs SET user_id = 1 WHERE user_id IS NULL"
    )

    op.alter_column(
        'jobs',
        'user_id',
        existing_type=sa.Integer(),
        nullable=False
    )

    op.create_foreign_key(
        'fk_jobs_user_id_users',
        'jobs',
        'users',
        ['user_id'],
        ['id']
    )

def downgrade() -> None:
    op.drop_constraint(
        'fk_jobs_user_id_users',
        'jobs',
        type_='foreignkey'
    )

    op.drop_column('jobs', 'user_id')