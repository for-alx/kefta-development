#!/usr/bin/python3
"""
"""
from models import db
from models.question import Question
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
import json


question = Blueprint('question', __name__)


@question.route('/question/<string:exam_id>', methods=['GET', 'POST'])
@login_required
def questions(exam_id):
	all_question = Question.query.filter_by(exam_id=exam_id).all()
	print(all_question)
	return render_template('question.html', user=current_user, questions=all_question)


@question.route('/add_question', methods=['GET', 'POST'])
@login_required
def add_question():
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

			# print('======================')
			# print(next_btn)
			# print(done_btn)
			# print('======================')
			# print(question, correct_answer, option2, option3, option4)

			new_question = Question(question=question, correct_option=correct_answer, option2=option2, option3=option3, option4=option4, exam_id=str(new_exam_id))
			db.session.add(new_question)
			db.session.commit()
			if next_btn == 'next':
				flash('Question created.', category='success')
				return redirect(url_for('question.add_question', exam_id=new_exam_id))
			else:
				flash('All question created.', category='success')
				return redirect(url_for('classes.class_s'))
			
	return render_template('add_question.html', user=current_user)
