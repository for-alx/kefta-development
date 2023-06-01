#!/usr/bin/python3
"""
"""
from models import db
from models.class_ import Class
from models.exam import Exam
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json


exam = Blueprint('exam', __name__)


@exam.route('/exam/<string:class_id>', methods=['GET', 'POST'])
@login_required
def exams(class_id):
    """ List all class for specific class """
    all_exam = Exam.query.filter_by(class_id=class_id).all()
    current_class = Class.query.filter_by(id=class_id).first()
    return render_template('exam.html', user=current_user, exams=all_exam, current_class=current_class)


@exam.route('/add_exam', methods=['GET', 'POST'])
@login_required
def add_exam():
    """ Add new exam for specific class """
    if current_user.__class__.__name__ == 'Teacher':
        new_class_id = request.args.get('class_id')
        if request.method == 'POST':
            exam_name = request.form.get('exam-name')
            new_exam = Exam(name=exam_name, class_id=str(new_class_id))
            db.session.add(new_exam)
            db.session.commit()
            flash('Exam created.', category='success')
            return redirect(url_for('question.add_question', exam_id=new_exam.id))
        return render_template('add_exam.html', user=current_user)
    else:
        flash('Students can\'t create exam.', category='error')
        return redirect(url_for('classes.class_s'))


@exam.route('/delete_exam/<string:exam_id>')
@login_required
def delete_exam(exam_id):
    if current_user.__class__.__name__ == 'Teacher':
        delete_obj = Exam.query.filter_by(id=exam_id).first()
        if delete_obj:
            class_id = delete_obj.class_id
            db.session.delete(delete_obj)
            db.session.commit()
            print('===============================================')
            print('\t======> Exam deleted <======')
            print('===============================================')
            flash('Exam deleted successfully', category='success')
            return  redirect(url_for('exam.exams', class_id=class_id))
        else:
            flash('Something is wrong.', category='error')
            return  redirect(url_for('exam.exams', class_id=class_id))
    else:
        flash('Students can\'t create classes.', category='error')
        return  redirect(url_for('exam.exams', class_id=class_id))


@exam.route('/edit_exam/<string:exam_id>', methods=['GET', 'POST'])
@login_required
def edit_exam(exam_id):
    if current_user.__class__.__name__ == 'Teacher':
        edit_obj = Exam.query.get(exam_id)
        if request.method == 'POST':
            exam_name = request.form.get('exam-name')
            edit_obj.name = exam_name
            db.session.add(edit_obj)
            db.session.commit()
            flash('Exam updated successfully.', category='success')
            return  redirect(url_for('exam.exams', class_id=edit_obj.class_id))

        if edit_obj:
            return render_template('edit_exam.html', user=current_user, edit_exam=edit_obj)
        else:
            flash('Some thing is wrong!', category='error')
            return redirect(url_for('classes.class_s'))
    else:
        flash('Students can\'t create classes.', category='error')
        return  redirect(url_for('exam.exams', class_id=edit_obj.class_id))
