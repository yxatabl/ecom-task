"""init_tables

Revision ID: 08ebee7433c7
Revises: 
Create Date: 2026-05-18 15:46:09.952971

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08ebee7433c7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            fullname TEXT NOT NULL,
            "group" TEXT NOT NULL,
            CONSTRAINT uq_name_group UNIQUE (fullname, "group")
        );
    """)

    op.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id SERIAL PRIMARY KEY,
            student_id INTEGER,
            "date" DATE,
            grade INTEGER NOT NULL,

            FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
        );
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE grades;")
    op.execute("DROP TABLE students;")
