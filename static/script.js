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

            const tagsHTML = todo.tags ? todo.tags.split(',').map(tag => `<span class="tag">${tag.trim()}</span>`).join('') : '';

            li.innerHTML = `
                <div class="todo-content">
                    <input type="checkbox" ${todo.todo_done ? 'checked' : ''}>
                    <span class="text">${todo.todo_text}</span>
                </div>
                <div class="todo-meta">
                    ${todo.todo_date ? `<span class="due-date">${new Date(todo.todo_date).toLocaleDateString()}</span>` : ''}
                    <div class="tags-container">${tagsHTML}</div>
                </div>
                <button class="delete-btn">Delete</button>
            `;
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
