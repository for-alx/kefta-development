#!/usr/bin/python3
"""
"""
from datetime import datetime
from models import db, generate_uuid


class Mark(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    mark = db.Column(db.Float, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'),
                           nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)

    def __repr__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
