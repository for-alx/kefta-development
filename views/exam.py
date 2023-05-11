#!/usr/bin/python3
"""
"""
from models import db
# from models.student import Class
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
    return render_template('exam.html', user=current_user, exams=all_exam)


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