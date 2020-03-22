from sqlalchemy import create_engine, select
from mapsdb import schema 

import os

URI = os.environ['SQLALCHEMY_DATABASE_URI']

engine = create_engine(URI)
conn = engine.connect()

s = select([schema.transitions])
result = conn.execute(s)
for row in result.fetchall():
    print(row)

s = select([schema.disks])
result = conn.execute(s)
for row in result.fetchall():
    print(row)