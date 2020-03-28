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
with engine.begin() as conn:

    # fill in the simple spw table
    for i in range(8):
        conn.execute(schema.spws.insert().values(spw_id=i))

    # fill in the bands
    conn.execute(schema.bands.insert().values(band_id=3))
    conn.execute(schema.bands.insert().values(band_id=6))

    # fill in the setups
    for i in range(2):
        conn.execute(schema.setups.insert().values(setup_id=i))


    # get all the unique keys of molecule names
    mol_list = set()
    for key, value in line_dict.items():
        for key in value.keys():
            mol_list.add(key)

    for mol in mol_list:
        conn.execute(schema.molecules.insert().values(molecule_name=mol))

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
                for transition_letter, vvdict in vdict.items():
                    conn.execute(
                        schema.transitions.insert().values(
                        frequency=vvdict["freq"],
                        molecule_name=mol,
                        transition_letter=transition_letter,
                        quantum_number=vvdict["qn"],
                        spw_id=int(vvdict["spw"]),
                        band_id=band,
                        setup_id=setup,
                    ))
            else:
                # there is no transition letter if we didn't
                # jump to a lower level
                conn.execute(
                    schema.transitions.insert().values(
                    frequency=vdict["freq"],
                    molecule_name=mol,
                    transition_letter=None, 
                    quantum_number=vdict["qn"],
                    spw_id=int(vdict["spw"]),
                    band_id=band,
                    setup_id=setup,
                ))


    for v in disk_dict.values():
        conn.execute(
            schema.disks.insert().values(
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
        ))

    # insert the reference table keys
    # prepped: run parameters entered into dictionary, sbatch scripts prepared
    # submitted: sbatch scripts submitted, queuing 
    # running: mpol running on GPU
    # failed: something went wrong during the running stage
    # mpol_completed: mpol finished, waiting to be plotted
    # plot_completed: plots successfully generated from mpol output
    for i, status in enumerate(["prepped", "submitted", "running",  "failed", "mpol_completed", "plot_completed"]):
        conn.execute(schema.run_statuses.insert().values(run_status_id=i, run_status=status))

    for i, method_type in enumerate(["tclean", "rml"]):
        conn.execute(schema.method_types.insert().values(method_type_id=i, method_type=method_type))


    conn.execute(schema.method_implementations.insert().values(method_type=0, method_version="v1")) # tclean v1
    conn.execute(schema.method_implementations.insert().values(method_type=0,  method_version="v2")) # tclean v2
    conn.execute(schema.method_implementations.insert().values(method_type=1, method_version=0)) # RML unspecified version

    # cube types 
    for i, image_type in enumerate(["image", "background", "dirty", "vis", "amplitude", "plot"]):
        conn.execute(schema.image_types.insert().values(image_type_id=i, image_type=image_type))
