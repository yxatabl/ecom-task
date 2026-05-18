from contextlib import asynccontextmanager

from asyncpg import Connection

from src.commons.postgres import Postgres


class UnitOfWork:
    def __init__(self, postgres: Postgres):
        self.postgres: Postgres = postgres
        self.conn: Connection = None
    
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
    def current_connection(self) -> Connection:
        return self.conn