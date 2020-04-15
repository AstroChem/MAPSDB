import os
from mapsdb import schema
from sqlalchemy import create_engine, select, and_

# query the schema for the disks, bands, and setup nums
URI = os.environ["SQLALCHEMY_DATABASE_URI"]

engine = create_engine(URI)

ms_id = 1
with engine.begin() as conn:
    s = select([schema.measurement_sets])
    result = conn.execute(s)

    for row in result.fetchall():
        print(row)
        # ms_id += 1

        # s = (
        #     schema.measurement_sets.update()
        #     .where(
        #         and_(
        #             (schema.measurement_sets.c.version == row["version"]),
        #             and_(
        #                 (
        #                     schema.measurement_sets.c.transition_id
        #                     == row["transition_id"]
        #                 ),
        #                 (schema.measurement_sets.c.disk_id == row["disk_id"]),
        #             ),
        #         )
        #     )
        #     .values(measurement_set_id=ms_id)
        # )
        # conn.execute(s)
