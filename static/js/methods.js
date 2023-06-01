// $(document).ready({
// 	// alert('import succed')
// 	console.log('Import succed')
// })

function examList(class_id) {
	// console.log('Class ID:', class_id)
	window.location.href = `/exam/${class_id}`;
}

function questionList(exam_id) {
	window.location.href = `/question/${exam_id}`;
}

function add_exam(class_id) {
	window.location.href = `/add_exam?class_id=${class_id}`;
}
function add_question(exam_id) {
	window.location.href = `/add_question?exam_id=${exam_id}`;
}


// Delete functions
function deleteClass(class_id) {
	window.location.href = `/delete_class/${class_id}`;
}
function deleteExam(exam_id) {
	window.location.href = `/delete_exam/${exam_id}`;
}
function deleteQuestion(question_id) {
	window.location.href = `/delete_question/${question_id}`;
}


// Edit functions
function editClass(class_id) {
	window.location.href = `/edit_class/${class_id}`;
}
function editExam(exam_id) {
	window.location.href = `/edit_exam/${exam_id}`;
}
function editQuestion(question_id) {
	window.location.href = `/edit_question/${question_id}`;
}