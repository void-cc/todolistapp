document.addEventListener('DOMContentLoaded', () => {
    const todoInput = document.getElementById('todo-input');
    const addBtn = document.getElementById('add-btn');
    const todoList = document.getElementById('todo-list');

    const fetchTodos = async () => {
        try {
            const response = await fetch('/api/todos');
            if (!response.ok) throw new Error('Failed to fetch todos');
            const todos = await response.json();
            renderTodos(todos);
        } catch (error) {
            console.error(error);
            alert('Failed to load todos.');
        }
    };

    const renderTodos = (todos) => {
        todoList.innerHTML = '';
        todos.forEach(todo => {
            const li = document.createElement('li');
            li.className = 'todo-item';
            li.dataset.id = todo.id;
            li.innerHTML = `
                <input type="checkbox" ${todo.todo_done ? 'checked' : ''}>
                <span class="text">${todo.todo_text}</span>
                <button class="delete-btn">Delete</button>
            `;
            todoList.appendChild(li);
        });
    };

    const addTodo = async () => {
        const text = todoInput.value.trim();
        if (text) {
            const tempId = Date.now();
            const newTodo = { id: tempId, todo_text: text, todo_done: false };

            const li = document.createElement('li');
            li.className = 'todo-item';
            li.dataset.id = tempId;
            li.innerHTML = `
                <input type="checkbox">
                <span class="text">${text}</span>
                <button class="delete-btn">Delete</button>
            `;
            todoList.appendChild(li);

            todoInput.value = '';

            try {
                const response = await fetch('/api/todos', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ todo_text: text })
                });
                if (!response.ok) throw new Error('Failed to add todo');
                fetchTodos();
            } catch (error) {
                console.error(error);
                alert('Failed to add todo. Please try again.');
                fetchTodos();
            }
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
        } catch (error) {
            console.error(error);
            alert('Failed to update todo. Please try again.');
            fetchTodos();
        }
    };

    const deleteTodo = async (id) => {
        const item = todoList.querySelector(`[data-id='${id}']`);
        if (item) {
            item.remove();
        }

        try {
            const response = await fetch(`/api/todos/${id}`, {
                method: 'DELETE'
            });
            if (!response.ok) throw new Error('Failed to delete todo');
        } catch (error) {
            console.error(error);
            alert('Failed to delete todo. Please try again.');
            fetchTodos();
        }
    };

    addBtn.addEventListener('click', addTodo);
    todoInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTodo();
        }
    });

    todoList.addEventListener('click', (e) => {
        const target = e.target;
        const item = target.closest('.todo-item');
        if (!item) return;

        const id = item.dataset.id;
        if (target.matches('.delete-btn')) {
            deleteTodo(id);
        } else if (target.matches('input[type="checkbox"]')) {
            const checked = target.checked;
            updateTodo(id, { todo_done: checked });
        }
    });

    fetchTodos();
});
