"""Specifies the base metadata registry for the database schema."""
from sqlalchemy.ext.declarative import declarative_base


Relation = declarative_base() #pylint: disable=invalid-name
