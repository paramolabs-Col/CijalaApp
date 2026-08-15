let allTodos = [];
let prioFilter = '';
const prioLabel = { urgent:'Urgente', medium:'Medio', low:'Pendiente' };

async function loadTodos(){
  const res = await fetch('/api/todos');
  allTodos = await res.json();
  renderTodos();
}

function renderTodos(){
  const showDone = document.getElementById('showDone').checked;
  const list = document.getElementById('todosList');

  const filtered = allTodos.filter(t => {
    if (prioFilter && t.priority !== prioFilter) return false;
    if (!showDone && t.done) return false;
    return true;
  });

  const byPrio = ['urgent','medium','low'];
  filtered.sort((a,b) => {
    if (a.done !== b.done) return a.done ? 1 : -1;
    return byPrio.indexOf(a.priority) - byPrio.indexOf(b.priority);
  });

  if (!filtered.length){
    list.innerHTML = `<div class="empty-state">${allTodos.length ? 'No hay tareas con ese filtro.' : 'Sin tareas todavía. Agregá la primera con el botón de abajo.'}</div>`;
    return;
  }

  list.innerHTML = filtered.map(t => `
    <div class="todo-card ${t.priority} ${t.done ? 'done' : ''}" data-id="${t.id}">
      <input type="checkbox" class="todo-cb" ${t.done ? 'checked' : ''}>
      <div class="todo-body">
        <div class="todo-text"></div>
        <div class="todo-meta">
          <span class="todo-prio-tag">
            <span class="semaforo ${t.priority}"></span>${prioLabel[t.priority] || t.priority}
          </span>
        </div>
      </div>
      <div class="todo-actions">
        <button class="todo-del" title="Eliminar">✕</button>
      </div>
    </div>
  `).join('');

  list.querySelectorAll('.todo-card').forEach(card => {
    const todo = allTodos.find(t => t.id === card.dataset.id);
    card.querySelector('.todo-text').textContent = todo.text;

    card.querySelector('.todo-cb').addEventListener('change', async (e) => {
      await fetch(`/api/todos/${todo.id}`, {
        method:'PUT', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({done: e.target.checked})
      });
      todo.done = e.target.checked;
      renderTodos();
    });

    card.querySelector('.todo-del').addEventListener('click', async () => {
      if (!confirm('¿Eliminar esta tarea?')) return;
      await fetch(`/api/todos/${todo.id}`, {method:'DELETE'});
      allTodos = allTodos.filter(t => t.id !== todo.id);
      renderTodos();
    });
  });
}

/* Filtros de prioridad */
document.querySelectorAll('.prio-filter').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.prio-filter').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    prioFilter = btn.dataset.p;
    renderTodos();
  });
});

document.getElementById('showDone').addEventListener('change', renderTodos);

/* Formulario nueva tarea */
let selectedPrio = 'urgent';

document.querySelectorAll('.prio-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.prio-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedPrio = btn.dataset.p;
  });
});

document.getElementById('todoForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const text = document.getElementById('todoText').value.trim();
  if (!text) return;

  const res = await fetch('/api/todos', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({text, priority: selectedPrio})
  });
  const todo = await res.json();
  allTodos.unshift(todo);
  document.getElementById('todoText').value = '';
  hideTodoForm();
  renderTodos();
});

document.getElementById('todoCancelBtn').addEventListener('click', hideTodoForm);

function showTodoForm(){
  const form = document.getElementById('todoForm');
  form.hidden = false;
  document.getElementById('todoText').focus();
}

function hideTodoForm(){
  document.getElementById('todoForm').hidden = true;
}
