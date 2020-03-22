from sqlalchemy import create_engine, select
import schema 


engine = create_engine("sqlite:///MAPS.db")
conn = engine.connect()

s = select([schema.transitions])
result = conn.execute(s)
for row in result.fetchall():
    print(row)

s = select([schema.disks])
result = conn.execute(s)
for row in result.fetchall():
    print(row)