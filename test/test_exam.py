import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import login_user, current_user
from models import db
from models.class_ import Class
from models.exam import Exam
from app import exam


class ExamTestCase(TestCase):
	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		app.config['SECRET_KEY'] = 'secret_key'
		db.init_app(app)
		app.register_blueprint(exam)
		return app

	def setUp(self):
		db.create_all()
		# Create a test teacher
		teacher = Teacher(email='admin@admin.com')
		db.session.add(teacher)
		db.session.commit()
		# Log in the test teacher
		login_user(teacher)
		# Create a test class
		test_class = Class(name='Test Class', teacher_id=teacher.id)
		db.session.add(test_class)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_exams_route(self):
		with self.client:
			response = self.client.get('/exam/1')
			self.assert200(response)
			self.assert_template_used('exam.html')

	def test_add_exam_route_teacher(self):
		with self.client:
			response = self.client.get('/add_exam?class_id=1')
			self.assert200(response)
			self.assert_template_used('add_exam.html')
			response = self.client.post('/add_exam', data={
				'exam-name': 'Test Exam'
			})
			self.assertRedirects(response, '/question/add_question/exam_id=1')

	def test_add_exam_route_student(self):
		with self.client:
			# Log out the teacher
			self.client.get('/logout')
			# Create a test student
			student = Student(email='student@example.com')
			db.session.add(student)
			db.session.commit()
			# Log in the test student
			login_user(student)
			response = self.client.get('/add_exam?class_id=1')
			self.assertRedirects(response, '/exam/1')
			response = self.client.post('/add_exam', data={
				'exam-name': 'Test Exam'
			})
			self.assertRedirects(response, '/exam/1')

	def test_delete_exam_route_teacher(self):
		with self.client:
			# Create a test exam
			test_exam = Exam(name='Test Exam', class_id=1)
			db.session.add(test_exam)
			db.session.commit()
			response = self.client.get(f'/delete_exam/{test_exam.id}')
			self.assertRedirects(response, '/exam/1')

	def test_delete_exam_route_student(self):
		with self.client:
			# Log out the teacher
			self.client.get('/logout')
			# Create a test student
			student = Student(email='student@example.com')
			db.session.add(student)
			db.session.commit()
			# Log in the test student
			login_user(student)
			response = self.client.get('/delete_exam/1')
			self.assertRedirects(response, '/exam/1')

	def test_edit_exam_route_teacher(self):
		with self.client:
			# Create a test exam
			test_exam = Exam(name='Test Exam', class_id=1)
			db.session.add(test_exam)
			db.session.commit()
			response = self.client.get(f'/edit_exam/{test_exam.id}')
			self.assert200(response)
			self.assert_template_used('edit_exam.html')
			response = self.client.post(f'/edit_exam/{test_exam.id}', data={
				'exam-name': 'Updated Test Exam'
			})
			self.assertRedirects(response, '/exam/1')

	def test_edit_exam_route_student(self):
		with self.client:
			# Log out the teacher
			self.client.get('/logout')
			# Create a test student
			student = Student(email='student@example.com')
			db.session.add(student)
			db.session.commit()
			# Log in the test student
			login_user(student)
			response = self.client.get('/edit_exam/1')
			self.assertRedirects(response, '/exam/1')
			response = self.client.post('/edit_exam/1', data={
				'exam-name': 'Updated Test Exam'
			})
			self.assertRedirects(response, '/exam/1')

if __name__ == '__main__':
	unittest.main()
