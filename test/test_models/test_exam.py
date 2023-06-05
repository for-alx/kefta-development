import unittest
from datetime import datetime
from models import db
from models.exam import Exam


class ExamTestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_exam_creation(self):
        # Create a test class
        test_class = Class(name='Test Class')
        db.session.add(test_class)
        db.session.commit()
        # Create a test exam
        test_exam = Exam(name='Test Exam', class_id=test_class.id)
        db.session.add(test_exam)
        db.session.commit()
        self.assertEqual(test_exam.name, 'Test Exam')
        self.assertIsInstance(test_exam.created_at, datetime)
        self.assertEqual(test_exam.class_id, test_class.id)
        self.assertIsInstance(test_exam.created_at, datetime)
        self.assertIsInstance(test_exam.updated_at, datetime)
        self.assertEqual(test_exam.questions, [])
        self.assertEqual(test_exam.marks, [])

    def test_exam_representation(self):
        test_exam = Exam(name='Test Exam', class_id='class_id')
        representation = repr(test_exam)
        expected_representation = "[Exam] ({id}) {data}".format(
            id=test_exam.id, data=test_exam.__dict__)
        self.assertEqual(representation, expected_representation)

    def test_student_no(self):
        test_exam = Exam(name='Test Exam', class_id='class_id')
        self.assertEqual(test_exam.student_no(), 0)
        # Create a test mark
        mark = Mark(exam_id=test_exam.id)
        db.session.add(mark)
        db.session.commit()
        self.assertEqual(test_exam.student_no(), 1)

    def test_student_no_with_multiple_marks(self):
        test_exam = Exam(name='Test Exam', class_id='class_id')
        self.assertEqual(test_exam.student_no(), 0)
        # Create multiple test marks
        marks = [
            Mark(exam_id=test_exam.id),
            Mark(exam_id=test_exam.id),
            Mark(exam_id=test_exam.id)
        ]
        db.session.add_all(marks)
        db.session.commit()
        self.assertEqual(test_exam.student_no(), 3)


if __name__ == '__main__':
    unittest.main()