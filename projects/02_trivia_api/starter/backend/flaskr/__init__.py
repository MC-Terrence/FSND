import os
import sys
from flask import Flask, json, request, abort, jsonify
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

# Pagination helper function


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

    # create and configure the app


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,True')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'PUT,DELETE,POST,GET')
        return response

    # Get all categories
    @app.route('/categories')
    def show_categories():
        categories = Category.query.order_by(Category.id).all()
        list_category = {}
        for cat in categories:
            list_category.update({cat.id: cat.type})
        return jsonify({
            'success': True,
            'total_categories': len(list_category),
            'categories': list_category
        })

# get all questions or search result if any
    @app.route('/questions')
    def retrieve_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.all()
        categories_object = {}  # translate category from list to dictionary object
        for cat in categories:
            categories_object.update({cat.id: cat.type})

        if not current_questions:  # page exceeds questions displayed
            abort(404)

        selection = Question.query.all()
        return jsonify({
            'success': True,
            'questions_on_this_page': len(current_questions),
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories_object,
            'current_category': None
        })

    # Delete question based on Question ID entered
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question is None:  # question referenced doesn't exist
            abort(404)
        try:
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(Question.query.all())
            })
        except BaseException:
            print(sys.exc_info())
            abort(422)

    # enter new question
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        if body:
            if body.get(
                    'searchTerm'):  # get searchterm from POST request body if available
                selection = Question.query.order_by(
                    Question.id).filter(
                    Question.question.ilike(
                        '%{}%'.format(body.get('searchTerm')))).all()
                if not selection:  # no matching search term
                    abort(404)

                current_questions = paginate_questions(
                    request, selection)  # matching search term
                if not current_questions:  # wrong search page indicated
                    abort(404)

                return jsonify({
                    'search string': body.get('searchTerm'),
                    'success': True,
                    'questions': current_questions,
                    'search_result_on_this_page': len(current_questions),
                    'total search result': len(selection)
                })

            else:

                new_question = body.get('question', None)
                new_answer = body.get('answer', None)
                new_category = body.get('category', None)
                new_difficulty = body.get('difficulty', None)

                try:
                    new_entry = Question(
                        question=new_question,
                        answer=new_answer,
                        category=new_category,
                        difficulty=new_difficulty)
                    new_entry.insert()

                    selection = Question.query.order_by(Question.id).all()
                    current_questions = paginate_questions(request, selection)

                    return jsonify({
                        'success': True,
                        'created': new_entry.id,
                        'questions': current_questions,
                        'total questions': len(Question.query.all())
                    })

                except BaseException:
                    abort(422)
        else:
            abort(400)

    # get questions in selected category
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_per_category(category_id):
        try:
            selection = db.session.query(Question).filter(
                Question.category == category_id).all()
            current_questions = paginate_questions(request, selection)
            return jsonify({
                'success': True,
                'total_questions': len(selection),
                'questions': current_questions,
                'current_category': category_id
            })
        except BaseException:
            abort(422)

    # retrieve random question
    @app.route('/quizzes', methods=['POST'])
    def play_trivia():
        body = request.get_json()
        if not body:  # if no body in request
            abort(400)
        try:
            trivia_category = body.get('trivia_category', None)
            previous_questions = body.get('previous_questions', None)
            if previous_questions is None:  # no previous question output
                if trivia_category:  # if category selected
                    category_questions = db.session.query(Question).filter(
                        Question.category == trivia_category).all()
                    random_question = random.choice(category_questions)
                    return jsonify({
                        'success': True,
                        'question': random_question.question
                    })
                else:  # no category selected
                    category_questions = db.session.query(Question).all()
                    random_question = random.choice(category_questions)
                    return jsonify({
                        'success': True,
                        'question': random_question.question
                    })
            else:  # previous question included in body
                if trivia_category:  # if category selected
                    category_questions = db.session.query(Question).filter(
                        Question.category == trivia_category).filter(
                        Question.id.notin_(previous_questions)).all()
                    random_question = random.choice(category_questions)
                    return jsonify({
                        'success': True,
                        'question': random_question.question
                    })
                else:  # no category selected
                    category_questions = db.session.query(Question).filter(
                        Question.id.notin_(previous_questions)).all()
                    random_question = random.choice(category_questions)
                    return jsonify({
                        'success': True,
                        'question': random_question.question
                    })
        except BaseException:
            print(sys.exc_info())
            abort(422)

    # error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not Found'
        }), 404

    @app.errorhandler(422)
    def not_processible(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Request unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request, please correct and resubmit request'
        }), 400

    return app
