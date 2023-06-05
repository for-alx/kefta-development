#!/usr/bin/python3
"""
"""
from models import db
from models.question import Question
from models.exam import Exam
from models.mark import Mark
from flask import Blueprint, render_template, request
from flask import flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json


question = Blueprint('question', __name__)


@question.route('/question/<string:exam_id>', methods=['GET', 'POST'])
@login_required
def questions(exam_id):
    """ """
    if request.method == 'POST':
        mark = 0
        req_data = request.get_json()
        req_data.get('answers').remove({})
        for answer in req_data.get('answers'):
            question_id = answer.get('questionId')
            answer = answer.get('answer')
            question = Question.query.filter_by(id=question_id).first()
            if question.correct_option == answer:
                mark = mark + 1
        mark_obj = Mark.query.filter_by(student_id=current_user.id, exam_id=question.exam_id).first()
        print('================')
        print(mark_obj)
        if mark_obj is None:
            new_obj = Mark(mark=mark, student_id=current_user.id, exam_id=question.exam_id)
            db.session.add(new_obj)
            db.session.commit()
        else:
            mark_obj.mark = mark
            db.session.add(mark_obj)
            db.session.commit()
            
        return str(mark)

    all_question = Question.query.filter_by(exam_id=exam_id).all()
    current_exam = Exam.query.filter_by(id=exam_id).first()
    return render_template('question.html', user=current_user,
                           questions=all_question, current_exam=current_exam)


@question.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
    """ """
    if current_user.__class__.__name__ == 'Teacher':
        new_exam_id = request.args.get('exam_id')
        print('From here 1 ', new_exam_id)
        if request.method == 'POST':
            question = request.form.get('question')
            correct_answer = request.form.get('correct-option')
            option2 = request.form.get('option2')
            option3 = request.form.get('option3')
            option4 = request.form.get('option4')
            next_btn = request.form.get('next-btn')
            done_btn = request.form.get('done-btn')

            new_question = Question(question=question,
                                    correct_option=correct_answer,
                                    option2=option2, option3=option3,
                                    option4=option4,
                                    exam_id=str(new_exam_id))
            db.session.add(new_question)
            db.session.commit()
            if next_btn == 'next':
                flash('Question created.', category='success')
                return redirect(url_for('question.add_question',
                                        exam_id=new_exam_id))
            else:
                flash('All question created.', category='success')
                return redirect(url_for('classes.class_s'))

    return render_template('add_question.html', user=current_user)


@question.route('/delete_question/<string:question_id>')
@login_required
def delete_question(question_id):
    """ """
    if current_user.__class__.__name__ == 'Teacher':
        delete_obj = Question.query.filter_by(id=question_id).first()
        if delete_obj:
            exam_id = delete_obj.exam_id
            db.session.delete(delete_obj)
            db.session.commit()
            print('===============================================')
            print('\t======> Question deleted <======')
            print('===============================================')
            flash('Question deleted successfully', category='success')
            return redirect(url_for('question.questions', exam_id=exam_id))
        else:
            flash('Something is wrong.', category='error')
            return redirect(url_for('question.questions', exam_id=exam_id))
    else:
        flash('Students can\'t create classes.', category='error')
        return redirect(url_for('question.questions', exam_id=exam_id))


@question.route('/edit_question/<string:question_id>', methods=['GET', 'POST'])
@login_required
def edit_question(question_id):
    """ """
    if current_user.__class__.__name__ == 'Teacher':
        edit_obj = Question.query.get(question_id)
        if request.method == 'POST':
            question = request.form.get('question')
            correct_answer = request.form.get('correct-option')
            option2 = request.form.get('option2')
            option3 = request.form.get('option3')
            option4 = request.form.get('option4')

            edit_obj.question = question
            edit_obj.correct_option = correct_answer
            edit_obj.option2 = option2
            edit_obj.option3 = option3
            edit_obj.option4 = option4

            db.session.add(edit_obj)
            db.session.commit()
            flash('Question updated successfully', category='success')
            return redirect(url_for('question.questions',
                                    exam_id=edit_obj.exam_id))

        if edit_obj:
            return render_template('edit_question.html', user=current_user,
                                   edit_question=edit_obj)
        else:
            flash('Some thing is wrong!', category='error')
            return redirect(url_for('classes.class_s'))
    else:
        flash('Students can\'t create classes.', category='error')
        return redirect(url_for('exam.exams', class_id=edit_obj.class_id))
