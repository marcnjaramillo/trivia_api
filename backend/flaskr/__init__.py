import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# method used by Caryn for pagination in the project lesson


def paginate_questions(request, all_questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in all_questions]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r'*': {'origins': '*'}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

#==========================================================================#
# ENDPOINTS
#==========================================================================#

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = {
            category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    @app.route('/questions', methods=['GET'])
    def get_paginated_questions():
        all_questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, all_questions)
        categories = Category.query.all()
        formatted_categories = {
            category.id: category.type for category in categories}

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': formatted_categories,
            'current_category': None
        })

    # I changed the endpoint because it didn't make sense to me. Since we are filtering questions based on category, it made more sense for the endpoint to be grouped with the other question endpoints.
    @app.route('/questions/category/<int:category_id>', methods=['GET'])
    def get_questions_by_category(category_id):
        try:

            all_questions = Question.query.filter_by(
                category=category_id).order_by(Question.id).all()
            current_questions = paginate_questions(request, all_questions)

            if category_id is None:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'current_category': category_id
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = body.get('searchTerm', '')

        try:
            all_questions = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(search)))
            current_questions = paginate_questions(request, all_questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'current_category': None
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            question = Question(question=new_question, answer=new_answer,
                                difficulty=new_difficulty, category=new_category)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id,
                'total_questions': len(Question.query.all())
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id,
                'total_questions': len(Question.query.all())
            })
        except Exception as e:
            print(e)
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
        print(body)

        try:
            if quiz_category['id'] == 0:
                filtered_questions = Question.query.all()
            else:
                filtered_questions = Question.query.filter_by(
                    category=quiz_category['id']).all()

            quiz_questions = []

            for question in filtered_questions:
                if question.id not in previous_questions:
                    quiz_questions.append(question.format())

            if len(quiz_questions) != 0:
                result = random.choice(quiz_questions)
                return jsonify({
                    'success': True,
                    'question': result
                })
            else:
                return jsonify({
                    'question': False
                })
        except Exception as e:
            print(e)
            abort(422)

#==========================================================================#
#  ERROR HANDLERS
#==========================================================================#

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(401)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500

    return app
