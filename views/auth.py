#!/usr/bin/python3
"""
"""
from flask_login import login_required, current_user, logout_user, login_user
from flask import Blueprint, render_template, request
from flask import flash, jsonify, redirect, url_for
from models import db
from models.student import Student
from werkzeug.security import generate_password_hash, check_password_hash
from models.teacher import Teacher

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        student = Student.query.filter_by(email=email).first()
        teacher = Teacher.query.filter_by(email=email).first()
        if student:
            if check_password_hash(student.password, password):
                flash('Logged in successfully!', category='success')
                login_user(student, remember=True)
                # return redirect(url_for('views.home'))
                # return 'Logged in as student'
                return redirect(url_for('classes.class_s'))

            else:
                flash('Incorrect password, try again.', category='error')
        elif teacher:
            if check_password_hash(teacher.password, password):
                flash('Logged in successfully!', category='success')
                login_user(teacher, remember=True)
                if current_user.email == 'admin@admin.com':
                    return redirect(url_for('classes.admin_route'))
                return redirect(url_for('classes.class_s'))
                # return 'Logged in as teacher'
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    if current_user.is_authenticated:
        return redirect(url_for('classes.class_s'))
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('classes.home'))


@auth.route('sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user_type = request.form.get('user-type')
        # Don't forget to implement user_type variable
        # if it's 'student' or 'teacher'

        student = Student.query.filter_by(email=email).first()
        teacher = Teacher.query.filter_by(email=email).first()
        if student or teacher:
            flash('Email already exists.', category='error')
        elif len(email) < 6:
            flash('Email must be greater than 6 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.',
                  category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            if user_type == 'student':
                new_student = Student(first_name=first_name,
                                      last_name=last_name,
                                      email=email,
                                      password=generate_password_hash(
                                        password1, method='sha256'))
                db.session.add(new_student)
                db.session.commit()
                login_user(new_student, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('classes.class_s'))
                # return 'account created'
            elif user_type == 'teacher':
                new_teacher = Teacher(first_name=first_name,
                                      last_name=last_name,
                                      email=email,
                                      password=generate_password_hash(
                                        password1, method='sha256'))
                db.session.add(new_teacher)
                db.session.commit()
                login_user(new_teacher, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('classes.class_s'))
                # return 'account created'

    return render_template("sign_up.html", user=current_user)


@auth.route('/secret')
@login_required
def secret():
    # return redirect(url_for('auth.login'))
    return 'secret message'
