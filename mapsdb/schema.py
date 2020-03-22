from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint
)

metadata = MetaData()


spws = Table("spws", metadata, Column("spw_id", Integer(), primary_key=True))

bands = Table("bands", metadata, Column("band_id", Integer(), primary_key=True))

setups = Table("setups", metadata, Column("setup_id", Integer(), primary_key=True))

# molecule names like HCO, C18O, etc...
molecules = Table(
    "molecules",
    metadata,
    Column("molecule_name", String(), unique=True, primary_key=True),
)

# Transitions of molecules, like C18O J=3-2
transitions = Table(
    "transitions",
    metadata,
    Column("transition_id", Integer(), primary_key=True),
    Column("frequency", Float(), nullable=False, unique=True),
    Column("mol_id", ForeignKey("molecules.molecule_name")),
    Column("quantum_number", String()),
    Column("spw_id", ForeignKey("spws.spw_id")),
    Column("band_id", ForeignKey("bands.band_id")),
    Column("setup_id", ForeignKey("setups.setup_id"))
)

disks = Table(
    "disks",
    metadata,
    Column("disk_id", Integer(), primary_key=True),
    Column("disk_name", String(), nullable=False, unique=True),
    Column("distance", Float()),
    Column("incl", Float()),
    Column("PA", Float()),
    Column("PA_gofish", Float()),
    Column("T_eff", Float()),
    Column("L_star", Float()),
    Column("M_star", Float()),
    Column("logMdot", Float()),
    Column("v_sys", Float()),
    Column("CO_ext", Float()),
    Column("RA_center", String()),
    Column("Dec_center", String()),
)

measurement_sets = Table(
    "measurement_sets",
    metadata,
    Column("transition_id", ForeignKey("transitions.transition_id")),
    Column("disk_id", ForeignKey("disks.disk_id")),
    Column("path", String(), unique=True),
    Column("version", String()),
    Column("ingested", DateTime()),
    PrimaryKeyConstraint("disk_id", "transition_id", "version", name="ms_id")
)
