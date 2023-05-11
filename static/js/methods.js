// $(document).ready({
// 	// alert('import succed')
// 	console.log('Import succed')
// })

function examList(id) {
	// console.log('Class ID:', id)
	window.location.href = `exam/${id}`;

}

function questionList(id) {
	// console.log('Exam ID: ', id)
	window.location.href = `/question/${id}`;

}