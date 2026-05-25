"""rls_policies

Revision ID: 0003
Revises: 0002
Create Date: 2026-05-24 23:54:00.000000

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None

def upgrade():
    # RLS is enabled for jobs, applications, cv, cover_letter, interview_prep, recruiter, audit_log
    
    op.execute("CREATE SCHEMA IF NOT EXISTS auth;")
    op.execute("""
    CREATE OR REPLACE FUNCTION auth.uid() RETURNS uuid AS $$
    BEGIN
        RETURN '00000000-0000-0000-0000-000000000000'::uuid;
    END;
    $$ LANGUAGE plpgsql;
    """)

    op.execute("""
    DO $$ 
    BEGIN 
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'authenticated') THEN 
            CREATE ROLE authenticated nologin noinherit; 
        END IF; 
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'service_role') THEN 
            CREATE ROLE service_role nologin noinherit bypassrls; 
        END IF; 
    END $$;
    """)

    # Enable RLS on all tables
    tables = [
        "jobs", "applications", "cvs", "cover_letters", "interview_preps", "recruiters"
    ]
    for table in tables:
        op.execute(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY;")
        
    # jobs: readable by all authenticated, writable by service role
    op.execute("CREATE POLICY jobs_select_policy ON jobs FOR SELECT TO authenticated USING (true);")
    op.execute("CREATE POLICY jobs_all_service_policy ON jobs FOR ALL TO service_role USING (true) WITH CHECK (true);")

    # applications: user-scoped via auth.uid() = user_id
    user_scoped_tables = ["applications"]
    for table in user_scoped_tables:
        op.execute(f"CREATE POLICY {table}_user_policy ON {table} FOR ALL TO authenticated USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);")

    # recruiters: shared read, service role write
    op.execute("CREATE POLICY recruiters_select_policy ON recruiters FOR SELECT TO authenticated USING (true);")
    op.execute("CREATE POLICY recruiters_all_service_policy ON recruiters FOR ALL TO service_role USING (true) WITH CHECK (true);")

def downgrade():
    tables = [
        "jobs", "applications", "cvs", "cover_letters", "interview_preps", "recruiters"
    ]
    
    op.execute("DROP POLICY IF EXISTS jobs_select_policy ON jobs;")
    op.execute("DROP POLICY IF EXISTS jobs_all_service_policy ON jobs;")
    
    for table in ["applications"]:
        op.execute(f"DROP POLICY IF EXISTS {table}_user_policy ON {table};")
        
    op.execute("DROP POLICY IF EXISTS recruiters_select_policy ON recruiters;")
    op.execute("DROP POLICY IF EXISTS recruiters_all_service_policy ON recruiters;")
    
    for table in tables:
        op.execute(f"ALTER TABLE {table} DISABLE ROW LEVEL SECURITY;")
