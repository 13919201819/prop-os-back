import logging
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings

logger = logging.getLogger("propos.db")

# Mask password in DATABASE_URL for secure logging
masked_url = settings.DATABASE_URL
if "@" in masked_url and "://" in masked_url:
    protocol_part, rest = masked_url.split("://", 1)
    creds, host_part = rest.split("@", 1)
    user = creds.split(":")[0] if ":" in creds else creds
    masked_url = f"{protocol_part}://{user}:*****@{host_part}"

logger.info(f"Initializing Async Database Engine with target: {masked_url}")

try:
    connect_args = {}
    if "postgresql" in settings.DATABASE_URL:
        connect_args = {"connect_timeout": 3}

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args=connect_args
    )
    logger.info("Database Engine initialized successfully.")
except Exception as e:
    logger.error(f"Failed to create Database Engine: {str(e)}", exc_info=True)
    raise e


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

async def get_db() -> AsyncGenerator[Optional[AsyncSession], None]:
    session = None
    try:
        session = AsyncSessionLocal()
        yield session
    except Exception:
        if session:
            try:
                await session.rollback()
            except Exception:
                pass
        raise
    finally:
        if session:
            try:
                await session.close()
            except Exception:
                pass


