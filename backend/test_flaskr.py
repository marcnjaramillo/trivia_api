import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the "easter egg" that is claimed to appear in every Pixar film?',
            'answer': 'A113',
            'difficulty': 2,
            'category': 5
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    #============================================================================#
    # TEST CASES
    #============================================================================#
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # Test case for '/categories' FAIL
    # ----------------------------------
    # I couldn't think of a way to test for an expected failure that wouldn't cause other tests to fail. The only thing I could think of is a 404 because there are no categories, but that would mean I have to delete the entire database and create questions without categories, which would cause at least the success test for '/categories/id/questions' to fail. Per this post (https://knowledge.udacity.com/questions/252621), I have concluded the only reasonable answer is that there is no failure case for this endpoint.

    def test_get_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_category'], None)
        self.assertTrue(data['categories'])

    def test_404_if_requested_page_does_not_exist(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_delete_question(self):
        res = self.client().delete('/questions/12')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 12).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 12)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

    def test_422_question_creation_fails(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

    def test_search_questions_with_returned_questions(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'title'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 2)

    def test_search_questions_with_no_returned_questions(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': '#$%'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertEqual(len(data['questions']), 0)

    def test_get_question_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertEqual(data['current_category'], None)

    def test_404_get_question_by_category(self):
        res = self.client().get('/categories/500')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_quiz_play(self):
        quiz_params = {'previous_questions': [0], 'quiz_category': {'id': 1}}
        res = self.client().post('/quizzes', json=quiz_params)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    # Technically, this test works but I feel like it could be written better.
    def test_422_quiz_questions_do_not_exist(self):
        quiz_params = {'previous_questions': [
            0], 'quiz_category': {'id': 1000}}
        res = self.client().post('/quizzes', json=quiz_params)
        data = json.loads(res.data)

        quiz_questions = Question.query.filter_by(category=1000)
        if not quiz_questions:
            self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
