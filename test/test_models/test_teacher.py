import unittest
from datetime import datetime
from models import db
from models.teacher import Teacher


class TeacherTestCase(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        db.create_all()

    def tearDown(self):
        """ """
        db.session.remove()
        db.drop_all()

    def test_teacher_creation(self):
        """ """
        # Create a test teacher
        test_teacher = Teacher(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            password='password123'
        )
        db.session.add(test_teacher)
        db.session.commit()
        self.assertEqual(test_teacher.first_name, 'John')
        self.assertEqual(test_teacher.last_name, 'Doe')
        self.assertEqual(test_teacher.email, 'johndoe@example.com')
        self.assertEqual(test_teacher.password, 'password123')

    def test_teacher_representation(self):
        """ """
        test_teacher = Teacher(
            first_name='John',
            last_name='Doe',
            email='johndoe@example.com',
            password='password123'
        )
        representation = repr(test_teacher)
        expected_representation = "[Teacher] ({id}) {data}".format(
            id=test_teacher.id, data=test_teacher.__dict__)
        self.assertEqual(representation, expected_representation)


if __name__ == '__main__':
    unittest.main()
