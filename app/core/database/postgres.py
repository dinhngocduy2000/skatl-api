from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncAttrs


from core.settings import settings as st

async def init_db(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class Base(AsyncAttrs, DeclarativeBase):
    pass


def create_pg_engine() -> AsyncEngine:
    engine = create_async_engine(
        st.pg_url,
    )
    return engine
