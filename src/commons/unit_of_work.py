from contextlib import asynccontextmanager

from src.commons.postgres import Postgres


class UnitOfWork:
    def __init__(self, postgres: Postgres):
        self.postgres = postgres
        self.conn = None
    
    @asynccontextmanager
    async def transaction(self):
        async with self.postgres.connection() as conn:
            self.conn = conn

            async with conn.transaction():
                try:
                    yield
                except Exception:
                    raise
                finally:
                    self.conn = None
    
    @property
    def current_connection(self):
        return self.conn