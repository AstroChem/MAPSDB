# MAPSDB
An SQLAlchemy implementation for storing information related to MAPS data processing


## Installation

pip install -e . 


## Database Migration

Using alembic. Make changes to schema in `mapsdb/schema.py`. Commit changes to git (not necessary, but good idea).



## Running

Before running any scripts, it's assumed that you have configured the following environment variable to point to the absolute path of the SQLITE database on your system.

    $ export SQLALCHEMY_DATABASE_URI="/path/to/your/data.db"

Note that for the SQLITE databases, four backslashes are needed to represent the absolute path. I.e.,

    $ export SQLALCHEMY_DATABASE_URI="sqlite:////Users/ianczekala/Documents/MAPS/MAPS.db"


---

Version : 
0.0.1.dev0