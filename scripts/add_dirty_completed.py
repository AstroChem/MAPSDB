import os

from sqlalchemy import create_engine

# insert the disk data
from diskdictionary import disk_dict
from linedictionary import line_dict
from mapsdb import schema

URI = os.environ["SQLALCHEMY_DATABASE_URI"]

engine = create_engine(URI)
with engine.begin() as conn:
    conn.execute(schema.run_statuses.insert().values(run_status="dirty_completed"))