"""initial

Revision ID: 0001
Revises: 
Create Date: 2026-05-24 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # enable vector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    op.create_table('jobs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('company', sa.String(), nullable=False),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('salary_min', sa.Integer(), nullable=True),
        sa.Column('salary_max', sa.Integer(), nullable=True),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('relevance_score', sa.Float(), nullable=True),
        sa.Column('embedding_status', sa.String(), nullable=False),
        sa.Column('saved', sa.Boolean(), nullable=False),
        sa.Column('scraped_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('embedding', pgvector.sqlalchemy.Vector(dim=1536), nullable=True),
        sa.Column('similarity_score', sa.Float(), nullable=True),
        sa.Column('job_structured', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_jobs_company'), 'jobs', ['company'], unique=False)
    op.create_index(op.f('ix_jobs_id'), 'jobs', ['id'], unique=False)
    op.create_index(op.f('ix_jobs_source'), 'jobs', ['source'], unique=False)
    op.create_index(op.f('ix_jobs_title'), 'jobs', ['title'], unique=False)
    op.create_index(op.f('ix_jobs_url'), 'jobs', ['url'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_jobs_url'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_title'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_source'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_id'), table_name='jobs')
    op.drop_index(op.f('ix_jobs_company'), table_name='jobs')
    op.drop_table('jobs')
