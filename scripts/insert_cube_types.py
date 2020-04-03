import os

from sqlalchemy import create_engine

# insert the disk data
from diskdictionary import disk_dict
from linedictionary import line_dict
from mapsdb import schema

URI = os.environ["SQLALCHEMY_DATABASE_URI"]

engine = create_engine(URI)
with engine.begin() as conn:

    # cube types 
    for i, cube_type in enumerate(["image", "background", "vis_full", "vis_cell", "amplitude"]):
        conn.execute(schema.cube_types.insert().values(cube_type_id=i, cube_type=cube_type))
