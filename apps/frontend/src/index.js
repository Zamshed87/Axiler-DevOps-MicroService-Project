// apps/frontend/src/index.js
const express = require('express');
const fetch = require('node-fetch');
const app = express();
const BACKEND = process.env.BACKEND_URL || "http://backend:5000";

app.use(express.json());
app.use(express.static(__dirname));

app.get('/api/proxy/todos', async (req, res) => {
  const r = await fetch(`${BACKEND}/todos`);
  const data = await r.json();
  res.json(data);
});

app.post('/api/proxy/todos', async (req, res) => {
  const r = await fetch(`${BACKEND}/todos`, {
    method: 'POST',
    headers: {'content-type':'application/json'},
    body: JSON.stringify(req.body)
  });
  const data = await r.json();
  res.status(r.status).json(data);
});

app.use('/', (req, res) => {
  res.send(`
  <!doctype html>
  <html>
  <head><meta charset="utf-8"><title>Todo</title></head>
  <body>
    <h1>Simple Todo</h1>
    <input id="t" placeholder="new todo"/>
    <button onclick="add()">Add</button>
    <ul id="list"></ul>
    <script>
      async function load(){
        const res = await fetch('/api/proxy/todos');
        const todos = await res.json();
        const ul = document.getElementById('list');
        ul.innerHTML = '';
        for(const t of todos){
          const li = document.createElement('li');
          li.textContent = t.title + (t.done ? ' ✅' : '');
          li.onclick = async () => {
            await fetch('/api/proxy/todos/'+t.id, {
              method:'PUT',
              headers:{'content-type':'application/json'},
              body: JSON.stringify({done: !t.done})
            });
            load();
          };
          ul.appendChild(li);
        }
      }
      async function add(){
        const input = document.getElementById('t');
        await fetch('/api/proxy/todos', {
          method:'POST',
          headers:{'content-type':'application/json'},
          body: JSON.stringify({title: input.value})
        });
        input.value = '';
        load();
      }
      load();
    </script>
  </body>
  </html>
  `);
});

const port = process.env.PORT || 8080;
app.listen(port, () => console.log('frontend listening', port));
