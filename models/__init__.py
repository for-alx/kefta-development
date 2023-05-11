from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def generate_uuid():
    """ Generate uuid id string """
    return str(uuid4())
