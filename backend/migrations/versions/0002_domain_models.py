"""domain models

Revision ID: 0002
Revises: 0001
Create Date: 2026-05-24 18:01:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import pgvector.sqlalchemy

revision: str = '0002'
down_revision: Union[str, None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # User Profiles
    op.create_table('user_profiles',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('target_role', sa.String(), nullable=False),
        sa.Column('target_location', sa.String(), nullable=False),
        sa.Column('skills', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('years_experience', sa.Integer(), nullable=False),
        sa.Column('cv_filename', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_profiles_id'), 'user_profiles', ['id'], unique=False)
    op.create_index(op.f('ix_user_profiles_email'), 'user_profiles', ['email'], unique=True)

    # Recruiters
    op.create_table('recruiters',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('company', sa.String(), nullable=False),
        sa.Column('linkedin_url', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('quality_score', sa.Float(), nullable=False),
        sa.Column('scraped_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recruiters_company'), 'recruiters', ['company'], unique=False)
    op.create_index(op.f('ix_recruiters_id'), 'recruiters', ['id'], unique=False)

    # Need to add recruiter_id to jobs
    op.add_column('jobs', sa.Column('recruiter_id', sa.UUID(), nullable=True))
    op.create_foreign_key(None, 'jobs', 'recruiters', ['recruiter_id'], ['id'])

    # Applications
    op.create_table('applications',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('job_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.Enum('draft', 'applied', 'awaiting_response', 'interviewing', 'offered', 'rejected', 'withdrawn', name='applicationstatus'), nullable=False),
        sa.Column('applied_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_applications_id'), 'applications', ['id'], unique=False)
    op.create_index(op.f('ix_applications_job_id'), 'applications', ['job_id'], unique=False)

    # CVs
    op.create_table('cvs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('embedding', pgvector.sqlalchemy.Vector(dim=1536), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cvs_id'), 'cvs', ['id'], unique=False)

    # Cover Letters
    op.create_table('cover_letters',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('job_id', sa.UUID(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('ats_keyword_match', sa.Float(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'generating', 'ready', 'failed', name='coverletterstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cover_letters_id'), 'cover_letters', ['id'], unique=False)
    op.create_index(op.f('ix_cover_letters_job_id'), 'cover_letters', ['job_id'], unique=False)

    # Scrape Runs
    op.create_table('scrape_runs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('source_id', sa.String(), nullable=False),
        sa.Column('jobs_found', sa.Integer(), nullable=False),
        sa.Column('jobs_inserted', sa.Integer(), nullable=False),
        sa.Column('duration_seconds', sa.Float(), nullable=False),
        sa.Column('run_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_scrape_runs_id'), 'scrape_runs', ['id'], unique=False)

    # Interview Preps
    op.create_table('interview_preps',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('job_id', sa.UUID(), nullable=False),
        sa.Column('questions', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('system_design_topics', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('salary_benchmark', sa.String(), nullable=True),
        sa.Column('company_research', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.Enum('pending', 'generating', 'ready', 'failed', name='interviewprepstatus'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_interview_preps_id'), 'interview_preps', ['id'], unique=False)
    op.create_index(op.f('ix_interview_preps_job_id'), 'interview_preps', ['job_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_interview_preps_job_id'), table_name='interview_preps')
    op.drop_index(op.f('ix_interview_preps_id'), table_name='interview_preps')
    op.drop_table('interview_preps')
    
    op.drop_index(op.f('ix_scrape_runs_id'), table_name='scrape_runs')
    op.drop_table('scrape_runs')
    
    op.drop_index(op.f('ix_cover_letters_job_id'), table_name='cover_letters')
    op.drop_index(op.f('ix_cover_letters_id'), table_name='cover_letters')
    op.drop_table('cover_letters')
    
    op.drop_index(op.f('ix_cvs_id'), table_name='cvs')
    op.drop_table('cvs')
    
    op.drop_index(op.f('ix_applications_job_id'), table_name='applications')
    op.drop_index(op.f('ix_applications_id'), table_name='applications')
    op.drop_table('applications')
    
    op.drop_constraint(None, 'jobs', type_='foreignkey')
    op.drop_column('jobs', 'recruiter_id')
    
    op.drop_index(op.f('ix_recruiters_id'), table_name='recruiters')
    op.drop_index(op.f('ix_recruiters_company'), table_name='recruiters')
    op.drop_table('recruiters')
    
    op.drop_index(op.f('ix_user_profiles_email'), table_name='user_profiles')
    op.drop_index(op.f('ix_user_profiles_id'), table_name='user_profiles')
    op.drop_table('user_profiles')
