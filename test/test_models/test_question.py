import unittest
from datetime import datetime
from models import db
from models.question import Question


class QuestionTestCase(unittest.TestCase):
    """ """
    def setUp(self):
        """ """
        db.create_all()

    def tearDown(self):
        """ """
        db.session.remove()
        db.drop_all()

    def test_question_creation(self):
        """ """
        # Create a test question
        test_question = Question(
            question='What is the capital of France?',
            correct_option='Paris',
            option2='London',
            option3='Berlin',
            option4='Rome',
            exam_id=1
        )
        db.session.add(test_question)
        db.session.commit()
        self.assertEqual(test_question.question,
                         'What is the capital of France?')
        self.assertEqual(test_question.correct_option, 'Paris')
        self.assertEqual(test_question.option2, 'London')
        self.assertEqual(test_question.option3, 'Berlin')
        self.assertEqual(test_question.option4, 'Rome')
        self.assertEqual(test_question.exam_id, 1)

    def test_question_representation(self):
        """ """
        test_question = Question(
            question='What is the capital of France?',
            correct_option='Paris',
            option2='London',
            option3='Berlin',
            option4='Rome',
            exam_id=1
        )
        representation = repr(test_question)
        expected_representation = "[Question] ({id}) {data}".format(
            id=test_question.id, data=test_question.__dict__)
        self.assertEqual(representation, expected_representation)


if __name__ == '__main__':
    unittest.main()
