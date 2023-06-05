import unittest
from datetime import datetime
from models import db
from models.class_ import Class


class ClassTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_class_creation(self):
        # Create a test teacher
        teacher = Teacher(email='teacher@example.com')
        db.session.add(teacher)
        db.session.commit()
        # Create a test class
        test_class = Class(name='Test Class', teacher_id=teacher.id,
                           image_name='test_image.jpg')
        db.session.add(test_class)
        db.session.commit()
        self.assertEqual(test_class.name, 'Test Class')
        self.assertEqual(test_class.teacher_id, teacher.id)
        self.assertIsInstance(test_class.created_at, datetime)
        self.assertIsInstance(test_class.updated_at, datetime)
        self.assertEqual(test_class.image_name, 'test_image.jpg')
        self.assertGreater(len(test_class.id), 0)
        self.assertEqual(test_class.exams, [])

    def test_class_representation(self):
        test_class = Class(name='Test Class', teacher_id='teacher_id',
                           image_name='test_image.jpg')
        representation = repr(test_class)
        expected_representation = "[Class] ({id}) {data}".format(
            id=test_class.id, data=test_class.__dict__)
        self.assertEqual(representation, expected_representation)


if __name__ == '__main__':
    unittest.main()
