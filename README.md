# MAPSDB
An SQLAlchemy implementation for storing information related to MAPS data processing


## Installation

pip install -e . 


## Database Migration

Using alembic. 

1. Make changes to schema in `mapsdb/schema.py`. 
2. Commit changes to git (not necessary, but good idea).
3. do autogeneration with $ alembic revision --autogenerate -m "message here". If the upgrade is tricky (including multiple primary key constraints, for example) do this manually by leaving --autogenerate off
4. Open `versions/XX_import_schema.py` and edit if necessary
5. apply with $ alembic upgrade head



## Running

Before running any scripts, it's assumed that you have configured the following environment variable to point to the absolute path of the SQLITE database on your system.

    $ export SQLALCHEMY_DATABASE_URI="/path/to/your/data.db"

Note that for the SQLITE databases, four backslashes are needed to represent the absolute path. I.e.,

    $ export SQLALCHEMY_DATABASE_URI="sqlite:////Users/ianczekala/Documents/MAPS/MAPS.db"


---

Version : 
0.0.1.dev0