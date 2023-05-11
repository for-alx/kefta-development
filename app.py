#!/usr/bin/python3
"""
"""
from models import db
from models.class_ import Class
from models.teacher import Teacher
from models.student import Student
from models.exam import Exam
from models.question import Question
from models.mark import Mark
from flask import Flask
from flask_login import LoginManager


DB_NAME = "database.db"


def create_app():
    """ Configure and  create flask app """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # register all blue prints
    from views.auth import auth
    from views.classes import classes
    from views.exam import exam
    from views.question import question

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(classes, url_prefix='/')
    app.register_blueprint(exam, url_prefix='/')
    app.register_blueprint(question, url_prefix='/')


    app.app_context().push()
    db.create_all()
    # with app.app_context():
    #     db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        if Student.query.get(id):
            return Student.query.get(id)
        elif Teacher.query.get(id):
            return Teacher.query.get(id)
        else:
            return None

    return app


app = create_app()
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
