function addTask() {
 var taskInput = document.getElementById('new-task');
 var taskText = taskInput.value;
 if (taskText === '') return;
 var taskList = document.getElementById('task-list');
 var listItem = document.createElement('li');
 listItem.textContent = taskText;
 var deleteButton = document.createElement('button');
 deleteButton.textContent = 'X';
 deleteButton.style.color = 'red';
 deleteButton.style.marginLeft = '10px';
 deleteButton.onclick = function() { taskList.removeChild(listItem); };
 listItem.appendChild(deleteButton);
 taskList.appendChild(listItem);
 taskInput.value = '';
}

var input = document.getElementById('new-task');
input.addEventListener('keypress', function(e) {
 if (e.key === 'Enter') {
 addTask();
 }
});
