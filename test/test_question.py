import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import login_user, current_user
from models import db
from models.question import Question
from models.exam import Exam
from app import question


class QuestionTestCase(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SECRET_KEY'] = 'secret_key'
        db.init_app(app)
        app.register_blueprint(question)
        return app
    def setUp(self):
        db.create_all()
        # Create a test teacher
        teacher = Teacher(email='admin@admin.com')
        db.session.add(teacher)
        db.session.commit()
        # Log in the test teacher
        login_user(teacher)
        # Create a test exam
        test_exam = Exam(name='Test Exam')
        db.session.add(test_exam)
        db.session.commit()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    def test_questions_route(self):
        with self.client:
            response = self.client.get('/question/1')
            self.assert200(response)
            self.assert_template_used('question.html')
    def test_add_question_route_teacher(self):
        with self.client:
            response = self.client.get('/add_question?exam_id=1')
            self.assert200(response)
            self.assert_template_used('add_question.html')
            response = self.client.post('/add_question', data={
                'question': 'Test Question',
                'correct-option': 'Option A',
                'option2': 'Option B',
                'option3': 'Option C',
                'option4': 'Option D',
                'next-btn': 'next'
            })
            self.assertRedirects(response, '/question/add_question/exam_id=1')
            response = self.client.post('/add_question', data={
                'question': 'Test Question',
                'correct-option': 'Option A',
                'option2': 'Option B',
                'option3': 'Option C',
                'option4': 'Option D',
                'done-btn': 'done'
            })
            self.assertRedirects(response, '/classes/class_s')
    def test_add_question_route_student(self):
        with self.client:
            # Log out the teacher
            self.client.get('/logout')
            # Create a test student
            student = Student(email='student@example.com')
            db.session.add(student)
            db.session.commit()
            # Log in the test student
            login_user(student)
            response = self.client.get('/add_question?exam_id=1')
            self.assertRedirects(response, '/question/1')
            response = self.client.post('/add_question', data={
                'question': 'Test Question',
                'correct-option': 'Option A',
                'option2': 'Option B',
                'option3': 'Option C',
                'option4': 'Option D',
                'next-btn': 'next'
            })
            self.assertRedirects(response, '/question/1')
            response = self.client.post('/add_question', data={
                'question': 'Test Question',
                'correct-option': 'Option A',
                'option2': 'Option B',
                'option3': 'Option C',
                'option4': 'Option D',
                'done-btn': 'done'
            })
            self.assertRedirects(response, '/question/1')
    def test_delete_question_route_teacher(self):
        with self.client:
            # Create a test question
            test_question = Question(question='Test Question',
            correct_option='Option A',
            option2='Option B',
            option3='Option C',
            option4='Option D',
            exam_id=1)
            db.session.add(test_question)
            db.session.commit()
            response = self.client.get('/delete_question/1')
            self.assertRedirects(response, '/question/1')
    def test_delete_question_route_student(self):
        with self.client:
            # Log out the teacher
            self.client.get('/logout')
            # Create a test student
            student = Student(email='student@example.com')
            db.session.add(student)
            db.session.commit()
            # Log in the test student
            login_user(student)
            response = self.client.get('/delete_question/1')
            self.assertRedirects(response, '/question/1')
    def test_edit_question_route_teacher(self):
        with self.client:
            # Create a test question
            test_question = Question(question='Test Question',
            correct_option='Option A',
            option2='Option B',
            option3='Option C',
            option4='Option D',
            exam_id=1)
            db.session.add(test_question)
            db.session.commit()
            response = self.client.get('/edit_question/1')
            self.assert200(response)
            self.assert_template_used('edit_question.html')
            response = self.client.post('/edit_question/1', data={
                'question': 'Updated Test Question',
                'correct-option': 'Updated Option A',
                'option2': 'Updated Option B',
                'option3': 'Updated Option C',
                'option4': 'Updated Option D'
            })
            self.assertRedirects(response, '/question/1')
    def test_edit_question_route_student(self):
        with self.client:
            # Log out the teacher
            self.client.get('/logout')
            # Create a test student
            student = Student(email='student@example.com')
            db.session.add(student)
            db.session.commit()
            # Log in the test student
            login_user(student)
            response = self.client.get('/edit_question/1')
            self.assertRedirects(response, '/question/1')
            response = self.client.post('/edit_question/1', data={
                'question': 'Updated Test Question',
                'correct-option': 'Updated Option A',
                'option2': 'Updated Option B',
                'option3': 'Updated Option C',
                'option4': 'Updated Option D'
            })
            self.assertRedirects(response, '/question/1')

if __name__ == '__main__':
    unittest.main()
