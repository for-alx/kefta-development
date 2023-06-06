import unittest
from datetime import datetime
from models import db
from models.student import Student


class StudentTestCase(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        db.create_all()

    def tearDown(self):
        """ """
        db.session.remove()
        db.drop_all()

    def test_student_creation(self):
        """ """
        # Create a test student
        test_student = Student(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            password='password123'
        )
        db.session.add(test_student)
        db.session.commit()
        self.assertEqual(test_student.first_name, 'John')
        self.assertEqual(test_student.last_name, 'Doe')
        self.assertEqual(test_student.email, 'johndoe@example.com')
        self.assertEqual(test_student.password, 'password123')

    def test_student_representation(self):
        """ """
        test_student = Student(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            password='password123'
        )
        representation = repr(test_student)
        expected_representation = "[Student] ({id}) {data}".format(
            id=test_student.id, data=test_student.__dict__)
        self.assertEqual(representation, expected_representation)


if __name__ == '__main__':
    unittest.main()
