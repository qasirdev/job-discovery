from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from backend.settings import get_settings
from backend.logging_config import get_logger

try:
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
    OTEL_SA_AVAILABLE = True
except ImportError:
    OTEL_SA_AVAILABLE = False

logger = get_logger("db")

class Base(AsyncAttrs, DeclarativeBase, MappedAsDataclass, kw_only=True):
    pass

_engine = None
_AsyncSessionLocal = None

def _get_engine():
    global _engine, _AsyncSessionLocal
    if _engine is None:
        settings = get_settings()
        # db.py must be importable without DATABASE_URL set, so we fetch it lazily
        db_url = str(settings.database_url) if settings.database_url else ""
        
        # Log pool creation event
        logger.info("creating_async_engine", pool_size=10, max_overflow=20)
        
        _engine = create_async_engine(
            db_url,
            echo=False,
            # pool_size=10 tuned to uvicorn --workers 2 (each worker owns its pool; total connections <= 20)
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            # pool_recycle=1800: prevents idle connection timeout from Supabase PgBouncer proxy
            pool_recycle=1800,
            # pool_pre_ping=True: validates connections before use; silently reconnects stale ones
            pool_pre_ping=True,
        )
        
        if OTEL_SA_AVAILABLE:
            SQLAlchemyInstrumentor().instrument(engine=_engine.sync_engine)
            
        _AsyncSessionLocal = async_sessionmaker(
            bind=_engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _AsyncSessionLocal

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency injection to get DB session."""
    session_maker = _get_engine()
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def close_db():
    """Gracefully dispose the async engine pool."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        logger.info("Database connection pool disposed")
