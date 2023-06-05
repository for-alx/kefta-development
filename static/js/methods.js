$(document).ready(function(){
	// alert('import succed')
  $(".send-answer").click(function(){
    $(".correct_answer").css("display", "block");
    console.log('button clicked')
  });

  $("#submitAnswers").click(function() {
  	let answers = [];
  	$("form").each(function() {
  		let questionId = $(this).data("question-id");
  		let selectedAnswer = $(this).find("input[name=answer]:checked").val();
  		answers.push({ questionId: questionId, answer: selectedAnswer });
  	});
  	$.ajax({
  		type: 'POST',
  		url: 'http://127.0.0.1:5000/question/answer',
  		data: JSON.stringify({answers}),
  		contentType: 'application/json',
  		success: function(result, status, xhr) {
  			console.log("Data: " + result + "\nStatus: " + status);
  			alert(`You get ${result} total score!`)
  			$(".correct_answer").css("display", "block")
  		}
  	});
  });

  $("#search-btn").click(function() {
  	let searchedWord = $("#search-word").val();
  	searchClass(searchedWord);
  })
});

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

// Search functions
function searchClass(name) {
	window.location.href = `/test/${name}`;
	// console.log(`from function ${name}`)
}
