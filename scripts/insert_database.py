"""
Insert all of the data contained in the line and disk dictionaries into the database.
"""

import os

from sqlalchemy import create_engine

# insert the disk data
from diskdictionary import disk_dict
from linedictionary import line_dict
from mapsdb import schema

URI = os.environ["SQLALCHEMY_DATABASE_URI"]

engine = create_engine(URI)
conn = engine.connect()

# fill in the simple spw table
for i in range(8):
    conn.execute(schema.spws.insert(), spw_id=i)

# fill in the bands
conn.execute(schema.bands.insert(), band_id=3)
conn.execute(schema.bands.insert(), band_id=6)

# fill in the setups
for i in range(2):
    conn.execute(schema.setups.insert(), setup_id=i)


# get all the unique keys of molecule names
mol_list = set()
for key, value in line_dict.items():
    for key in value.keys():
        mol_list.add(key)

for mol in mol_list:
    conn.execute(schema.molecules.insert(), molecule_name=mol)

# do setup1B3
setup_dict = {
    "Setup1B3": (1, 3),
    "Setup2B3": (2, 3),
    "Setup1B6": (1, 6),
    "Setup2B6": (2, 6),
}

for key, (setup, band) in setup_dict.items():
    d = line_dict[key]
    for mol, vdict in d.items():
        if "spw" not in vdict.keys():
            # go to a lower level
            for junk, vvdict in vdict.items():
                conn.execute(
                    schema.transitions.insert(),
                    frequency=vvdict["freq"],
                    mol_id=mol,
                    quantum_number=vvdict["qn"],
                    spw_id=int(vvdict["spw"]),
                    band_id=band,
                    setup_id=setup,
                )
        else:
            # insert the values
            conn.execute(
                schema.transitions.insert(),
                frequency=vdict["freq"],
                mol_id=mol,
                quantum_number=vdict["qn"],
                spw_id=int(vdict["spw"]),
                band_id=band,
                setup_id=setup,
            )


for v in disk_dict.values():
    conn.execute(
        schema.disks.insert(),
        disk_name=v["name"],
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

conn.close()