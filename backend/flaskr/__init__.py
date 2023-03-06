import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.get_categories()

        if len(categories) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "categories": categories
            }
        )
    
    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        categories = Category.get_categories()

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(current_questions),
                "categories": categories,
                "currentCategory": categories.get(1)
            }
        )


    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(Question.id == question_id).one_or_none()
        if question is None:
            abort(404)

        try:
            question.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": question_id
                }
            )

        except:
            print(sys.exc_info())
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_category = body.get("category", None)
        new_difficulty = body.get("difficulty", None)
       
        if new_category is None:
            abort(400)
        try:
            question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
            question.insert()

            return jsonify(
                {
                    "success": True,
                    "created": question.id
                }
            )

        except:
            print(sys.exc_info())
            abort(500)    

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        questions = Question.searchByQuestionText(search_term)

        return jsonify(
                {
                    "success": True,
                    "questions": questions,
                    "totalQuestions": len(questions),
                }
            )

        
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
       
        category = Category.getCategoryById(category_id)

        if category is None:
            abort(404)

        questions = Question.getQuestionsByCategoryId(category_id)
        return jsonify(
                {
                    "success": True,
                    "currentCategory": category.type,
                    "questions": questions,
                    "totalQuestions": len(questions),
                }
        )

    @app.route('/quizzes', methods=['POST'])
    def play_quizzes():
        body = request.get_json()
        previous_questions = body.get("previous_questions", [])
        quiz_category = body.get("quiz_category", None)
        category_id = quiz_category["id"]
        category = Category.getCategoryById(category_id)

        if category is None:
                questions = Question.query.filter(Question.id.not_in(previous_questions)).all()
        else:
                questions = Question.query.filter(Question.id.not_in(previous_questions), Question.category == category.id).all()

        formatted_questions = [question.format() for question in questions]
        if formatted_questions == []:
            return jsonify({
                "success": True
            })
        else:
            random_question = None
            random_question = random.choice(formatted_questions)

            return jsonify(
                {
                    "success": True,
                    "question": random_question
                }
            )
  

    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify(
            {
                "success": False,
                "error": 404,
                "message": "resource not found"}),
            404
        )

    @app.errorhandler(422)
    def unprocessableEntity(error):
        return (
            jsonify(
            {
                "success": False, 
                "error": 422,
                "message": "unprocessable entity"}),
            422
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify(
            {
                "success": False, 
                "error": 400,
                "message": "bad request"}),
            400
        )


    @app.errorhandler(500)
    def internal_error(error):
        return (
            jsonify(
            {  
                "success": False, 
                "error": 500,
                "message": "internal server error"}),
            500
        )


    return app

