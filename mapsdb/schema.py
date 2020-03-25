from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
    ForeignKeyConstraint
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

# meant to be a reference table of prepped, submitted, running, completed, analysis, etc.
run_statuses = Table(
    "run_statuses",
    metadata,
    Column("run_status_id", Integer(), primary_key=True),
    Column("run_status", String(), unique=True)
)

# reference table for tclean / RML
method_types = Table(
    "method_types",
    metadata,
    Column("method_type_id", Integer(), primary_key=True),
    Column("method_type", String(), unique=True)
)

# MPoL dev 0.5, or tclean v2
method_implementations = Table(
    "method_implementations",
    metadata,
    Column("method_type", ForeignKey("method_types.method_type")),
    Column("method_version", String()),
    PrimaryKeyConstraint("method_type", "method_version", name="method_implementation_id")
)

parameters = Table(
    "parameters",
    metadata,
    Column("parameter_id", Integer(), primary_key=True),
    Column("npix", Integer()),
    Column("cell_size", Float()),
    Column("n_opt", Integer()),
    Column("loss_rate", Float()),
    Column("penalty_entropy", Float()),
    Column("penalty_tsv", Float())
)

# summarizing how we prepare and track all SLURM runs for RML
runs = Table(
    "runs",
    metadata,
    Column("run_id", Integer(), primary_key=True),
    Column("run_status", ForeignKey("run_statuses.run_status_id")),
    Column("job_array_id", Integer()),
    Column("slurm_id", Integer()),
    Column("updated", DateTime()),
    Column("output_dir", String()),
    Column("channel_start", Integer()),
    Column("channel_end", Integer()),
    Column("parameter_id", ForeignKey("parameters.parameter_id")),
    Column("disk_id", Integer(), nullable=False),
    Column("transition_id", Integer(), nullable=False),
    Column("version", Integer(), nullable=False),
    ForeignKeyConstraint(["disk_id", "transition_id", "version"], ["measurement_sets.disk_id", "measurement_sets.transition_id", "measurement_sets.version"], name="ms_id"),
    Column("method_type", String()),
    Column("method_version", String()),
    ForeignKeyConstraint(["method_type", "method_version"], ["method_implementations.method_type", "method_implementations.method_version"], name="method_implementation_id")
)

# image, dirty_image, vis
cube_types = Table(
    "cube_types",
    metadata,
    Column("cube_type_id", Integer(), primary_key=True),
    Column("cube_type", String())
)

# for individual jpgs: plot, im, vis
img_types = Table(
    "img_types",
    metadata,
    Column("img_type_id", Integer(), primary_key=True),
    Column("img_type", String())
)

# referencing or will reference a collection of images (pngs or jpgs) made from one of the products. 
# # e.g., a dirty image,
cubes = Table(
    "cubes",
    metadata,
    Column("cube_id", Integer(), primary_key=True),
    Column("run_id", ForeignKey("runs.run_id")),
    Column("disk_id", Integer(), nullable=False),
    Column("transition_id", Integer(), nullable=False),
    Column("version", Integer(), nullable=False),
    ForeignKeyConstraint(["disk_id", "transition_id", "version"], ["measurement_sets.disk_id", "measurement_sets.transition_id", "measurement_sets.version"], name="ms_id"),
    Column("method_type", String()),
    Column("method_version", String()),
    ForeignKeyConstraint(["method_type", "method_version"], ["method_implementations.method_type", "method_implementations.method_version"], name="method_implementation_id")
)

images = Table(
    "images",
    metadata,
    Column("image_id", Integer(), primary_key=True),
    Column("cube_id", ForeignKey("cubes.cube_id")),
    Column("run_id", ForeignKey("runs.run_id")),
    Column("image_path", String()),
    Column("channel", Integer()),
    Column("velocity", Float())
)


