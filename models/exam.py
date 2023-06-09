#!/usr/bin/python3
"""
"""
from datetime import datetime
from models import db, generate_uuid
from models.mark import Mark


class Exam(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    class_id = db.Column(db.String(60), db.ForeignKey('class.id'),
                         nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    questions = db.relationship('Question', backref='exam', lazy=True,
                                cascade="all, delete-orphan")
    # added for mark if any problem couse by this line remove it
    marks = db.relationship('Mark', backref='exam', lazy=True,
                            cascade="all, delete-orphan")

    def __repr__(self):
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def student_no(self):
        return len(self.marks)
