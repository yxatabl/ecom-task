import asyncpg

import os

DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@database:5432/grades")

class Postgres:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(self.db_url)
    
    async def disconnect(self):
        if self.pool:
            self.pool.terminate()

database = Postgres(DB_URL)