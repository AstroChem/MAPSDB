"""changing column name to run_id


Revision ID: df88255c79ea
Revises: 47a0ac9c4af7
Create Date: 2020-03-24 22:17:00.230435

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df88255c79ea'
down_revision = '47a0ac9c4af7'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("runs", "runs_id", new_column_name="run_id")


def downgrade():
    op.alter_column("runs", "run_id", new_column_name="runs_id")
