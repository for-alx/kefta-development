#!/usr/bin/python3
"""
"""
from models import db
from models.class_ import Class
from models.teacher import Teacher
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json
from werkzeug.utils import secure_filename
import os
from uuid import uuid4


classes = Blueprint('classes', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpeg', 'jpg', 'gif'}
UPLOAD_FOLDER = 'static/user-data'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# =====================Test route==============
@classes.route('/test', methods=['GET', 'POST'])
def test_route():
    my_id = str(current_user.__class__.__name__)
    print(my_id)
    return ('id: {}'.format(my_id))
# =============================================


@classes.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user, home=True)


@classes.route('/class', methods=['GET', 'POST'])
@login_required
def class_s():
    all_class = Class.query.all()
    all_teachers = Teacher.query.all()
    return render_template('class.html', user=current_user, classes=all_class, teachers=all_teachers)


@classes.route('/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
    if current_user.__class__.__name__ == 'Teacher':
        if request.method == 'POST':
            teacher_id = str(current_user.id)
            class_name = request.form.get('class-name')
            new_file_name = str(uuid4())[:13]

            if len(class_name) < 3:
                flash('Class Name must be greater than 3 chars.', category='error')
            # file handle
            if 'file' not in request.files:
                flash('No file part', category='error')
            file = request.files['file']
            if file.filename == '':
                flash('No selected file', category='error')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))

                new_class = Class(name=class_name, teacher_id=teacher_id, image_name=filename)
                db.session.add(new_class)
                db.session.commit()
                flash('Class created.', category='success')
                return redirect(url_for('exam.add_exam', class_id=new_class.id))
        return render_template('add_class.html', user=current_user)
    else:
        flash('Students can\'t create classes.', category='error')
        return redirect(url_for('classes.class_s'))
