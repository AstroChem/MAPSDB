# run through and update the disk table with the latest properties in the disk dictionary
import os

from sqlalchemy import create_engine

# insert the disk data
# load the new disk dictionary
from diskdictionary import disk_dict
from linedictionary import line_dict
from mapsdb import schema

# replace all "names" with the correct spaced versions
# uses the key in disk_dict -> name
name_conv = {
    "GM_Aur": "GM Aur",
    "MWC_480": "MWC 480",
    "AS_209": "AS 209",
    "IM_Lup": "IM Lup",
    "HD_163296": "HD 163296",
}

URI = os.environ["SQLALCHEMY_DATABASE_URI"]


engine = create_engine(URI)
with engine.begin() as conn:

    for k, v in disk_dict.items():
        conn.execute(
            schema.disks.update()
            .where(schema.disks.c.disk_name == name_conv[k])
            .values(
                disk_name=name_conv[k],
                distance=v["distance"],
                incl=v["incl"],
                PA=v["PA"],
                PA_gofish=v["PA_gofish"],
                T_eff=v["Teff"],
                L_star=v["L_star"],
                M_star=v["M_star"],
                logMdot=v["logMdot"],
                v_sys=v["v_sys"],
                CO_ext=v["12CO_extent"],
                RA_center=v["RA_center"],
                Dec_center=v["Dec_center"],
            )
        )

conn.close()
