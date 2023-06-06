import unittest
from datetime import datetime
from models import db
from models.mark import Mark


class MarkTestCase(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        db.create_all()

    def tearDown(self):
        """ """
        db.session.remove()
        db.drop_all()

    def test_mark_creation(self):
        """ """
        # Create a test mark
        test_mark = Mark(mark=85.5, student_id=1, exam_id=1)
        db.session.add(test_mark)
        db.session.commit()
        self.assertEqual(test_mark.mark, 85.5)
        self.assertEqual(test_mark.student_id, 1)
        self.assertEqual(test_mark.exam_id, 1)

    def test_mark_representation(self):
        """ """
        test_mark = Mark(mark=85.5, student_id=1, exam_id=1)
        representation = repr(test_mark)
        expected_representation = "[Mark] ({id}) {data}".format(
            id=test_mark.id, data=test_mark.__dict__)
        self.assertEqual(representation, expected_representation)


if __name__ == '__main__':
    unittest.main()
