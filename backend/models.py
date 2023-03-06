import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = 'trivia'
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'abc')
database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD,'localhost:5432', database_name)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

"""
Question

"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }
    
    def searchByQuestionText(search_term):
        search_results = Question.query.filter(
            Question.question.ilike(f"%{search_term}%")
        ).all()
        questions = [question.format() for question in search_results]
        return questions  
    
    def getQuestionsByCategoryId(category_id):
        search_results = Question.query.filter(Question.category == category_id).all()
        questions = [question.format() for question in search_results]
        return questions  
    
    def getRandomQuestions(previous_questions, category_id):
        search_results = Question.query.filter(Question.category == category_id).all()
        questions = [question.format() for question in search_results]
        return questions 
    

"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }  

    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id: category.type for category in categories}
        return formatted_categories   
    
    def getCategoryById(category_id):
        category = Category.query.filter(Category.id == category_id).one_or_none()
        return category 
 
  
    
