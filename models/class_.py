#!/usr/bin/python3
"""
"""
from datetime import datetime
from models import db, generate_uuid


class Class(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(60), nullable=False)
    teacher_id = db.Column(db.String(60), db.ForeignKey('teacher.id'),
                           nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    image_name = db.Column(db.String(60), nullable=False)
    exams = db.relationship('Exam', backref='class', lazy=True)

    def __repr__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
