import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import login_user, current_user
from werkzeug.datastructures import ImmutableMultiDict
from models import db
from models.class_ import Class
from models.teacher import Teacher
from app import classes


class ClassesTestCase(TestCase):
    """ """
    def create_app(self):
        """ """
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['SECRET_KEY'] = 'secret_key'
        app.config['UPLOAD_FOLDER'] = 'static/user-data'
        db.init_app(app)
        app.register_blueprint(classes)
        return app

    def setUp(self):
        """ """
        db.create_all()
        # Create a test teacher
        teacher = Teacher(email='admin@admin.com')
        db.session.add(teacher)
        db.session.commit()
        # Log in the test teacher
        login_user(teacher)

    def tearDown(self):
        """ """
        db.session.remove()
        db.drop_all()

    def test_admin_route(self):
        """ """
        with self.client:
            response = self.client.get('/admin')
            self.assert200(response)
            self.assert_template_used('admin.html')
            self.assertIn(b'Not Allowed for users.', response.data)

    def test_home_route(self):
        """ """
        with self.client:
            response = self.client.get('/')
            self.assert200(response)
            self.assert_template_used('home.html')

    def test_class_s_route(self):
        """ """
        with self.client:
            response = self.client.get('/class')
            self.assert200(response)
            self.assert_template_used('class.html')

    def test_add_class_route_teacher(self):
        """ """
        with self.client:
            response = self.client.get('/add_class')
            self.assert200(response)
            self.assert_template_used('add_class.html')
            response = self.client.post('/add_class', data={
                'class-name': 'Test Class',
                'file': (open('test_image.jpg', 'rb'), 'test_image.jpg')
            }, content_type='multipart/form-data')
            self.assertRedirects(response, '/exam/add_exam/class_id=1')

    def test_add_class_route_student(self):
        """ """
        with self.client:
            # Log out the teacher
            self.client.get('/logout')
            # Create a test student
            student = Student(email='student@example.com')
            db.session.add(student)
            db.session.commit()
            # Log in the test student
            login_user(student)
            response = self.client.get('/add_class')
            self.assertRedirects(response, '/class')
            response = self.client.post('/add_class', data={
                'class-name': 'Test Class',
                'file': (open('test_image.jpg', 'rb'), 'test_image.jpg')
            }, content_type='multipart/form-data')
            self.assertRedirects(response, '/class')

    def test_edit_class_route_teacher(self):
        """ """
        with self.client:
            # Create a test class
            test_class = Class(name='Test Class', teacher_id=current_user.id)
            db.session.add(test_class)
            db.session.commit()
            response = self.client.get(f'/edit_class/{test_class.id}')
            self.assert200(response)
            self.assert_template_used('edit_class.html')
            response = self.client.post(f'/edit_class/{test_class.id}', data={
                'class-name': 'Updated Test Class',
                'file': (open('test_image.jpg', 'rb'), 'test_image.jpg')
            }, content_type='multipart/form-data')
            self.assertRedirects(response, '/class')

    def test_edit_class_route_student(self):
        """ """
        with self.client:
            # Log out the teacher
            self.client.get('/logout')
            # Create a test student
            student = Student(email='student@example.com')
            db.session.add(student)
            db.session.commit()
            # Log in the test student
            login_user(student)
            response = self.client.get('/edit_class/1')
            self.assertRedirects(response, '/class')
            response = self.client.post('/edit_class/1', data={
                'class-name': 'Updated Test Class',
                'file': (open('test_image.jpg', 'rb'), 'test_image.jpg')
            }, content_type='multipart/form-data')
            self.assertRedirects(response, '/class')

    def test_delete_class_route_teacher(self):
        """ """
        with self.client:
            # Create a test class
            test_class = Class(name='Test Class', teacher_id=current_user.id)
            db.session.add(test_class)
            db.session.commit()
            response = self.client.get(f'/delete_class/{test_class.id}')
            self.assertRedirects(response, '/class')

    def test_delete_class_route_student(self):
        """ """
        with self.client:
            # Log out the teacher
            self.client.get('/logout')
            # Create a test student
            student = Student(email='student@example.com')
            db.session.add(student)
            db.session.commit()
            # Log in the test student
            login_user(student)
            response = self.client.get('/delete_class/1')
            self.assertRedirects(response, '/class')


if __name__ == '__main__':
    unittest.main()
