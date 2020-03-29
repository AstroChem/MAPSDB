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

convention = {
  "ix": 'ix_%(column_0_label)s',
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

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
    Column("molecule_name", ForeignKey("molecules.molecule_name")),
    Column("transition_letter", String()),
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
    Column("tar_md5sum", String(), unique=True), # the md5sum corresponding to the .tar.gz file ingested. 
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
    Column("method_type_id", ForeignKey("method_types.method_type_id")),
    Column("method_version", String()),
    PrimaryKeyConstraint("method_type_id", "method_version", name="method_implementation_id")
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
    Column("run_status_id", ForeignKey("run_statuses.run_status_id")),
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
    Column("method_type_id", Integer()),
    Column("method_version", String()),
    ForeignKeyConstraint(["method_type_id", "method_version"], ["method_implementations.method_type_id", "method_implementations.method_version"], name="method_implementation_id")
)

# what is the image of? image, bkg, amp, vis, dirty, etc...
image_types = Table(
    "image_types",
    metadata,
    Column("image_type_id", Integer(), primary_key=True),
    Column("image_type", String(), unique=True)
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
    Column("method_type_id", Integer()),
    Column("method_version", String()),
    ForeignKeyConstraint(["method_type_id", "method_version"], ["method_implementations.method_type_id", "method_implementations.method_version"], name="method_implementation_id")
)

images = Table(
    "images",
    metadata,
    Column("image_id", Integer(), primary_key=True),
    Column("image_type_id", Integer(), ForeignKey("images.image_type_id")),
    Column("cube_id", ForeignKey("cubes.cube_id")),
    Column("run_id", ForeignKey("runs.run_id")),
    Column("image_path", String()),
    Column("channel", Integer()),
    Column("velocity", Float())
)


