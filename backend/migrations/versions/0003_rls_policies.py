"""rls_policies

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-24 23:54:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

def upgrade():
    # RLS is enabled for jobs, applications, cv, cover_letter, interview_prep, recruiter, audit_log
    
    # Enable RLS on all tables
    tables = [
        "jobs", "applications", "cv", "cover_letter", "interview_prep", "recruiter", "audit_log"
    ]
    for table in tables:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;")
        
    # jobs: readable by all authenticated, writable by service role
    op.execute("CREATE POLICY jobs_select_policy ON jobs FOR SELECT TO authenticated USING (true);")
    op.execute("CREATE POLICY jobs_all_service_policy ON jobs FOR ALL TO service_role USING (true) WITH CHECK (true);")

    # applications, cv, cover_letter, interview_prep: user-scoped via auth.uid() = user_id
    user_scoped_tables = ["applications", "cv", "cover_letter", "interview_prep"]
    for table in user_scoped_tables:
        op.execute(f"CREATE POLICY {table}_user_policy ON {table} FOR ALL TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);")

    # recruiter: shared read, service role write
    op.execute("CREATE POLICY recruiter_select_policy ON recruiter FOR SELECT TO authenticated USING (true);")
    op.execute("CREATE POLICY recruiter_all_service_policy ON recruiter FOR ALL TO service_role USING (true) WITH CHECK (true);")

    # audit_log: insert for authenticated/service, read/update/delete for service only
    op.execute("CREATE POLICY audit_log_insert_policy ON audit_log FOR INSERT TO authenticated, service_role WITH CHECK (true);")
    op.execute("CREATE POLICY audit_log_service_policy ON audit_log FOR ALL TO service_role USING (true) WITH CHECK (true);")

def downgrade():
    tables = [
        "jobs", "applications", "cv", "cover_letter", "interview_prep", "recruiter", "audit_log"
    ]
    
    op.execute("DROP POLICY IF EXISTS jobs_select_policy ON jobs;")
    op.execute("DROP POLICY IF EXISTS jobs_all_service_policy ON jobs;")
    
    for table in ["applications", "cv", "cover_letter", "interview_prep"]:
        op.execute(f"DROP POLICY IF EXISTS {table}_user_policy ON {table};")
        
    op.execute("DROP POLICY IF EXISTS recruiter_select_policy ON recruiter;")
    op.execute("DROP POLICY IF EXISTS recruiter_all_service_policy ON recruiter;")
    
    op.execute("DROP POLICY IF EXISTS audit_log_insert_policy ON audit_log;")
    op.execute("DROP POLICY IF EXISTS audit_log_service_policy ON audit_log;")
    
    for table in tables:
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;")
