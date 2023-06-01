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
    if current_user.email == 'admin@admin.com':
        all_class = Class.query.all()
        # User_email = current_user.email
        # print(User_email)
        return render_template('admin.html', user=current_user, classes=all_class)
    else:
        flash('Not Allowed for users.', category='error')
        return redirect(url_for('classes.class_s'))
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


@classes.route('/edit_class/<string:class_id>', methods=['GET', 'POST'])
@login_required
def edit_class(class_id):
    if current_user.__class__.__name__ == 'Teacher':
        edit_obj = Class.query.get(class_id)
        if request.method == 'POST':
            class_name = request.form.get('class-name')

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

                edit_obj.name = class_name
                edit_obj.image_name = filename

                db.session.add(edit_obj)
                db.session.commit()
                flash('Class updated successfully.', category='success')
                return redirect(url_for('classes.class_s'))

        if edit_obj:
            return render_template('edit_class.html', user=current_user, edit_class=edit_obj)
        else:
            flash('Some thing is wrong!', category='error')
            return redirect(url_for('classes.class_s'))


@classes.route('/delete_class/<string:class_id>')
@login_required
def delete_class(class_id):
    if current_user.__class__.__name__ == 'Teacher':
        delete_obj = Class.query.filter_by(id=class_id).first()
        db.session.delete(delete_obj)
        db.session.commit()
        # return f'Class delete {classes}'
        flash('Class deleted successfully', category='success')
        return redirect(url_for('classes.class_s'))
    else:
        flash('Students can\'t create classes.', category='error')
        return redirect(url_for('classes.class_s'))
    
