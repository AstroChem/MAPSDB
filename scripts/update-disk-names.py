# run through and update the disk table with the latest properties in the disk dictionary
import os

from sqlalchemy import create_engine, select

# insert the disk data
# load the new disk dictionary
from diskdictionary import disk_dict
from linedictionary import line_dict
from mapsdb import schema

# replace all "names" with the correct spaced versions
# uses the key in disk_dict -> name
name_conv = {
    "GM Aur": "GM Aur",
    "MWC_480": "MWC 480",
    "AS_209": "AS 209",
    "IM_Lup": "IM Lup",
    "HD_163296": "HD 163296",
}

URI = os.environ["SQLALCHEMY_DATABASE_URI"]

print("BEFORE")
engine = create_engine(URI)
with engine.begin() as conn:

    s = select([schema.disks])
    result = conn.execute(s)
    for row in result.fetchall():
        print(row)


engine = create_engine(URI)
with engine.begin() as conn:

    # iterate throught the keys of the disk dictionary
    for k, v in disk_dict.items():
        conn.execute(
            schema.disks.update()
            .where(schema.disks.c.disk_name == v["name"])
            .values(
                disk_name=name_conv[v["name"]]
            )
        )

print("AFTER")
engine = create_engine(URI)
with engine.begin() as conn:

    s = select([schema.disks])
    result = conn.execute(s)
    for row in result.fetchall():
        print(row)
