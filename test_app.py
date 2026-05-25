import asyncio
from sqlalchemy import select
from backend.db import _get_engine
from backend.models import Application, Job, ApplicationStatus
import uuid

async def test():
    session_maker = _get_engine()
    async with session_maker() as session:
        # Create a dummy job to link to
        j = Job(title="test", company="test", source="test", url="http://test.com", description="test")
        session.add(j)
        await session.flush()
        
        try:
            a = Application(
                job_id=j.id,
                user_id=uuid.UUID("00000000-0000-0000-0000-000000000000"),
                status="applied",
                notes="test"
            )
            session.add(a)
            await session.flush()
            print("Success")
        except Exception as e:
            print(f"Exception: {type(e).__name__}: {e}")

asyncio.run(test())
