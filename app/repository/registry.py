from typing import Callable, TypeVar

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

T = TypeVar("T")

class Registry:  # pylint: disable=too-many-instance-attributes
    _pg_engine: AsyncEngine
   

    def __init__(self, pg_engine: AsyncEngine):
        self._pg_engine = pg_engine
        # Construct the repository instances here
     

    async def do_tx(self, tx_func: Callable[[AsyncSession], T]) -> T:
        try:
            async_session = async_sessionmaker(
                self._pg_engine, expire_on_commit=False)
            session = async_session()
            await session.begin()
            res = await tx_func(session)
            await session.commit()
            return res
        except Exception as e:
            if session is not None and session.is_active:
                await session.rollback()
            raise e
        finally:
            if session is not None and session.is_active:
                await session.close()

    # Function to get the repository instance
   