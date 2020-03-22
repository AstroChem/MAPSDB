'''
This is no longer relevant, since the creation of the schema is done through alembic. But if we did need to create the schema via SQLAlchemy Core, this would be how.
'''

from sqlalchemy import create_engine
import os

URI = os.environ['SQLALCHEMY_DATABASE_URI']

from mapsdb import schema 

engine = create_engine(URI)
schema.metadata.create_all(engine)


