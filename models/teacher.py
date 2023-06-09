#!/usr/bin/python3
"""
"""
from flask_login import UserMixin
from datetime import datetime
from models import db, generate_uuid


class Teacher(db.Model, UserMixin):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    classes = db.relationship('Class', backref='teacher', lazy=True,
                              cascade="all, delete-orphan")

    def __repr__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
