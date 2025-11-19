document.addEventListener('DOMContentLoaded', () => {
    const todoInput = document.getElementById('todo-input');
    const todoDateInput = document.getElementById('todo-date');
    const todoTagsInput = document.getElementById('todo-tags');
    const addBtn = document.getElementById('add-btn');
    const todoList = document.getElementById('todo-list');

    const fetchTodos = async () => {
        try {
            const response = await fetch('/api/todos');
            if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = '/login';
                }
                throw new Error('Failed to fetch todos');
            }
            const todos = await response.json();
            renderTodos(todos);
        } catch (error) {
            console.error(error);
            // Don't alert here, as it can be annoying on page load
        }
    };

    const renderTodos = (todos) => {
        todoList.innerHTML = '';
        todos.forEach(todo => {
            const li = document.createElement('li');
            li.className = 'todo-item';
            li.dataset.id = todo.id;

            const isOverdue = todo.todo_date && new Date(todo.todo_date) < new Date();
            if (isOverdue) {
                li.classList.add('overdue');
            }
            if (todo.todo_done) {
                li.classList.add('completed');
            }

            // Create todo-content div
            const todoContentDiv = document.createElement('div');
            todoContentDiv.className = 'todo-content';

            // Checkbox
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            if (todo.todo_done) {
                checkbox.checked = true;
            }
            todoContentDiv.appendChild(checkbox);

            // Todo text
            const textSpan = document.createElement('span');
            textSpan.className = 'text';
            textSpan.textContent = todo.todo_text;
            todoContentDiv.appendChild(textSpan);

            // Create todo-meta div
            const todoMetaDiv = document.createElement('div');
            todoMetaDiv.className = 'todo-meta';

            // Due date
            if (todo.todo_date) {
                const dueDateSpan = document.createElement('span');
                dueDateSpan.className = 'due-date';
                dueDateSpan.textContent = new Date(todo.todo_date).toLocaleDateString();
                todoMetaDiv.appendChild(dueDateSpan);
            }

            // Tags
            const tagsContainer = document.createElement('div');
            tagsContainer.className = 'tags-container';
            if (todo.tags) {
                todo.tags.split(',').forEach(tag => {
                    const tagSpan = document.createElement('span');
                    tagSpan.className = 'tag';
                    tagSpan.textContent = tag.trim();
                    tagsContainer.appendChild(tagSpan);
                });
            }
            todoMetaDiv.appendChild(tagsContainer);

            // Delete button
            const deleteBtn = document.createElement('button');
            deleteBtn.className = 'delete-btn';
            deleteBtn.textContent = 'Delete';

            // Assemble
            li.appendChild(todoContentDiv);
            li.appendChild(todoMetaDiv);
            li.appendChild(deleteBtn);
            todoList.appendChild(li);
        });
    };

    const addTodo = async () => {
        const text = todoInput.value.trim();
        const date = todoDateInput.value;
        const tags = todoTagsInput.value.trim();

        if (!text) {
            alert('Todo text cannot be empty.');
            return;
        }

        const payload = {
            todo_text: text,
            todo_date: date || null,
            tags: tags || null,
        };

        try {
            const response = await fetch('/api/todos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error('Failed to add todo');

            todoInput.value = '';
            todoDateInput.value = '';
            todoTagsInput.value = '';

            fetchTodos();
        } catch (error) {
            console.error(error);
            alert('Failed to add todo. Please try again.');
        }
    };

    const updateTodo = async (id, data) => {
        try {
            const response = await fetch(`/api/todos/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error('Failed to update todo');
            // Optimistically update UI or just refetch
            fetchTodos();
        } catch (error) {
            console.error(error);
            alert('Failed to update todo. Please try again.');
        }
    };

    const deleteTodo = async (id) => {
        try {
            const response = await fetch(`/api/todos/${id}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error('Failed to delete todo');

            // Remove from UI
            const item = todoList.querySelector(`[data-id='${id}']`);
            if (item) item.remove();

        } catch (error) {
            console.error(error);
            alert('Failed to delete todo. Please try again.');
        }
    };

    addBtn.addEventListener('click', addTodo);
    todoInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') addTodo(); });
    todoDateInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') addTodo(); });
    todoTagsInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') addTodo(); });

    todoList.addEventListener('click', (e) => {
        const target = e.target;
        const item = target.closest('.todo-item');
        if (!item) return;

        const id = item.dataset.id;
        if (target.matches('.delete-btn')) {
            deleteTodo(id);
        } else if (target.matches('input[type="checkbox"]')) {
            const isDone = target.checked;
            updateTodo(id, { todo_done: isDone });
        }
    });

    fetchTodos();
});
