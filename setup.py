import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Read the version from the last line in the README
# This is the one location that the version is single-sourced
with open("README.md") as version_file:
    for line in version_file:
        pass
    version = line.strip()

setuptools.setup(
    name="mapsdb",
    version=version,
    author="Ian Czekala",
    author_email="iancze@gmail.com",
    description="SQL database for MAPS project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AstroChem/MAPSDB",
    install_requires=["numpy", "sqlalchemy", "alembic"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.5",
)