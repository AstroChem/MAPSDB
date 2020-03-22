from sqlalchemy import create_engine

import schema 

engine = create_engine("sqlite:///MAPS.db")
schema.metadata.create_all(engine)
