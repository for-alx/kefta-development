#!/usr/bin/python3
"""
"""
from datetime import datetime
from models import db, generate_uuid


class Question(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    question = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
