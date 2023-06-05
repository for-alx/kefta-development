import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import login_user
from werkzeug.datastructures import ImmutableMultiDict
from models import db
from models.student import Student
from models.teacher import Teacher
from app import auth



class AuthTestCase(TestCase):
	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		app.config['SECRET_KEY'] = 'secret_key'
		db.init_app(app)
		app.register_blueprint(auth)
		return app

	def setUp(self):
		db.create_all()
		# Create a test student
		student = Student(first_name='Test', last_name='Student', email='student@example.com',
		password='password')
		db.session.add(student)
		# Create a test teacher
		teacher = Teacher(first_name='Test', last_name='Teacher', email='teacher@example.com',
		password='password')
		db.session.add(teacher)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_login_success(self):
		with self.client:
			response = self.client.post('/login', data={
				'email': 'student@example.com',
				'password': 'password'
			})
			self.assertRedirects(response, '/class_s')

	def test_login_incorrect_password(self):
		with self.client:
			response = self.client.post('/login', data={
				'email': 'student@example.com',
				'password': 'incorrect_password'
			})
			self.assert200(response)
			self.assertIn(b'Incorrect password', response.data)

	def test_login_nonexistent_email(self):
		with self.client:
			response = self.client.post('/login', data={
				'email': 'nonexistent@example.com',
				'password': 'password'
			})
			self.assert200(response)
			self.assertIn(b'Email does not exist', response.data)

	def test_logout(self):
		with self.client:
			# Log in a student
			student = Student.query.filter_by(email='student@example.com').first()
			login_user(student)
			response = self.client.get('/logout')
			self.assertRedirects(response, '/home')

	def test_sign_up_success(self):
		with self.client:
			response = self.client.post('/sign_up', data={
				'firstName': 'New',
				'lastName': 'User',
				'email': 'newuser@example.com',
				'password1': 'password',
				'password2': 'password',
				'user-type': 'student'
			})
			self.assertRedirects(response, '/class_s')

	def test_sign_up_existing_email(self):
		with self.client:
			response = self.client.post('/sign_up', data={
				'firstName': 'New',
				'lastName': 'User',
				'email': 'student@example.com', # Existing email
				'password1': 'password',
				'password2': 'password',
				'user-type': 'student'
			})
			self.assert200(response)
			self.assertIn(b'Email already exists', response.data)

	def test_sign_up_invalid_email(self):
		with self.client:
			response = self.client.post('/sign_up', data={
				'firstName': 'New',
				'lastName': 'User',
				'email': 'invalid_email', # Invalid email
				'password1': 'password',
				'password2': 'password',
				'user-type': 'student'
			})
			self.assert200(response)
			self.assertIn(b'Email must be greater than 6 characters', response.data)

	def test_sign_up_invalid_first_name(self):
		with self.client:
			response = self.client.post('/sign_up', data={
				'firstName': 'A',
				'lastName': 'User',
				'email': 'newuser@example.com',
				'password1': 'password',
				'password2': 'password',
				'user-type': 'student'
			})
			self.assert200(response)
			self.assertIn(b'First name must be greater than 1 character', response.data)

	def test_sign_up_password_mismatch(self):
		with self.client:
			response = self.client.post('/sign_up', data={
				'firstName': 'New',
				'lastName': 'User',
				'email': 'newuser@example.com',
				'password1': 'password1',
				'password2': 'password2', # Passwords don't match
				'user-type': 'student'
			})
			self.assert200(response)
			self.assertIn(b'Passwords don\'t match', response.data)

	def test_sign_up_short_password(self):
		with self.client:
			response = self.client.post('/sign_up', data={
				'firstName': 'New',
				'lastName': 'User',
				'email': 'newuser@example.com',
				'password1': 'pass', # Password too short
				'password2': 'pass', # Password too short
				'user-type': 'student'
			})
			self.assert200(response)
			self.assertIn(b'Password must be at least 7 characters', response.data)

	def test_secret_page_authenticated(self):
		with self.client:
			# Log in a student
			student = Student.query.filter_by(email='student@example.com').first()
			login_user(student)
			response = self.client.get('/secret')
			self.assert200(response)
			self.assertEqual(response.data, b'secret message')

	def test_secret_page_unauthenticated(self):
		with self.client:
			response = self.client.get('/secret')
			self.assertRedirects(response, '/login')


if __name__ == '__main__':
	unittest.main()
