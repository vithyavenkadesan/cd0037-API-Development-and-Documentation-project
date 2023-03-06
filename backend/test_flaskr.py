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
        DB_USER = os.getenv('DB_USER', 'postgres')
        DB_PASSWORD = os.getenv('DB_PASSWORD', 'abc')
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,'localhost:5432', self.database_name)
      
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
 
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('categories'))

    def test_get_categories_error(self):
        res = self.client().get('/categoriess')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), 'resource not found')

    def test_get_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertGreater(data.get('totalQuestions'), 0)

    def test_get_questions_pagination_success(self):
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertGreater(data.get('totalQuestions'), 0)

    def test_delete_question_error(self):
        res = self.client().delete('/questions/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), 'resource not found')

    
    def test_create_question_success(self):
        requestBody = {
            'question': 'Who invented light',
            'answer': 'Edison',
            'category': 1,
            'difficulty': 5
        }
        res = self.client().post('/questions', json=requestBody)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertGreater(data.get('created'), 0)

    def test_create_question_error(self):
        requestBody = {
            'question': 'Who invented light',
            'answer': 'Edison',
            'difficulty': 5
        }
        res = self.client().post('/questions', json=requestBody)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data.get('success'), False)
        self.assertEqual(data.get('message'), 'bad request')

    def test_search_question_success(self):
        requestBody = {
            'searchTerm': 'Who'
        }
        res = self.client().post('/questions/search', json=requestBody)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertGreater(data.get('totalQuestions'), 0)

    
    def test_get_questions_by_category_success(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertGreater(data.get('totalQuestions'), 0)

    def test_get_questions_by_category_error(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data.get('success'), False)

    def test_play_quizzes_success(self):
        requestBody = {
            'quiz_category': {
                "type": "History", 
                 "id": 2
            }
        }
        res = self.client().post('/quizzes', json = requestBody)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('question'))

    def test_play_quizzes_without_category_success(self):
        requestBody = {
            'quiz_category': {
                "type": "click", 
                 "id": 0
            }
            }
        res = self.client().post('/quizzes', json = requestBody)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data.get('success'), True)
        self.assertTrue(data.get('question'))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()