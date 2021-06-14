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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_entry = {
            'question': 'Who dey brrreeet?',
            'answer': 'Davido',
            'category': 5,
            'difficulty': 5
        }

        self.play_parameters = {
            'trivia_category': 1,
            'previous_questions': 1
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions_on_this_page'])

    def test_get_invalid_page(self):
        res = self.client().get('/questions?page=100000', json={'search':'xyz'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'],'Resource not Found')
        self.assertEqual(data['success'], False)

    def test_get_valid_search(self):
        res = self.client().get('/questions?search=who', json={'search':'who'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['search string'], 'who')
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    def test_get_invalid_search(self):
        res = self.client().get('/questions?search=wxyz', json={'search': 'wxyz'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'],'Resource not Found')
        self.assertEqual(data['success'], False)

    def valid_create_question_request(self):
        res = self.client().post('/questions', json=self.new_entry)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    def test_valild_delete_question_request(self):
        res = self.client().delete('/questions/10')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 10)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question,None)

    def invalid_delete_question_request(self):
        res = self.client().delete('/questions/50000')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 50000).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'],'Resource not Found')
        self.assertEqual(data['success'], False)

    def invalid_create_question_request(self):
        res = self.client().post('/questions/5000', json={self.new_entry})
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    def test_play(self):
        res = self.client().post('/play', json={self.play_parameters})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']))
  
    def test_invalid_play_request(self): #request to play without body
        res = self.client().post('/play')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Bad request, please correct and resubmit request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()