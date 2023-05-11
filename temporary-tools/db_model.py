# RESOURCES

# https://www.digitalocean.com/community/tutorials/how-to-use-one-to-many-database-relationships-with-flask-sqlalchemy

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from uuid import uuid4


def generate_uuid():
    """ Generate uuid id string """
    return str(uuid4())


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    marks = db.relationship('Mark', backref='student', lazy=True)

class Teacher(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    classes = db.relationship('Class', backref='teacher', lazy=True)

class Class(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(60), nullable=True)
    teacher_id = db.Column(db.String(60), db.ForeignKey('teacher.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    exams = db.relationship('Exam', backref='class', lazy=True)

class Exam(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    class_id = db.Column(db.String(60), db.ForeignKey('class.id'), nullable=False)
    questions = db.relationship('Question', backref='exam', lazy=True)

class Question(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    text = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)

class Mark(db.Model):
    id = db.Column(db.String(60), primary_key=True, default=generate_uuid)
    mark = db.Column(db.Float, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'), nullable=False)


app.app_context().push()
# db.create_all()

# new_user = Student(first_name='ali4', last_name='ahmed', email='email8@mail.com', password='withoutpush')
# db.session.add(new_user)

# t1 = Teacher(first_name='My python', last_name='flask', email='python@mail.com', password='pypass')
# db.session.add(t1)

# c1 = Class(name='Python2', teacher_id='4f8021ee-5dca-43ca-bb52-9df7a285a6a')
# db.session.add(c1)

result = Teacher.query.all()

print(result)
for row in result:
    print(row.classes[0].name)





















# q1 = Question(text="what is the advantage of using flask?", answer='answer',)

# db.session.commit()

# db.create_all()
