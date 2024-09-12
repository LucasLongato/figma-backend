# Task Management
O gerenciador de tarefas é uma ferramenta que auxilia no planejamento, organização e acompanhamento de atividades ou tarefas. Ele permite que os usuários criem, visualizem, editem e monitorem suas tarefas, facilitando a gestão do tempo e a produtividade. Esse tipo de software pode ser usado tanto individualmente quanto em equipes, promovendo maior eficiência no trabalho.



O nosso gerenciador de tarefas ele tem as seguintes telas:

## login 

## cadastro 
## Local aonde fica as tarefas
## E o pop de criação das Tarefas:

para poder executar o programa acima deve ter o python instalado
Caso não tenha click no link https://www.python.org/downloads/
e deve estar com o flask instalado para rodar. Caso não esteja rodar esse comando no terminal.

/ pip install flask /

Usemos o Banco sqlite para armazenar os dados no banco.
Caso nao tenha o slite faça os seguintes passos para a instalação:

- Baixe o SQLite aqui (baixe a versão "Precompiled Binaries for Windows").
- Extraia o arquivo baixado em um diretório de sua escolha.
- Adicione o caminho do executável sqlite3.exe ao PATH do sistema para acessá-lo de qualquer terminal.



abaixo podemos ver alguns enpoints:

## Endpoints

### User Endpoints

#### POST /register

Registers a new user.

**Request Body:**
{
  "login": "leo",
  "password": "123"
}

**Responses:**
- 201 Created: {"message": "User registered successfully"}
- 400 Bad Request: {"error": "User already exists"}

---

#### POST /login

Logs in a user.

**Request Body:**
{
  "login": "leo",
  "password": "123"
}

**Responses:**
- 200 OK: {"message": "Logged in as leo"}
- 401 Unauthorized: {"error": "Invalid credentials"}

---

#### POST /logout

Logs out the current user.

**Responses:**
- 200 OK: {"message": "Logged out successfully"}

---

#### GET /

Returns a list of all users.

**Responses:**
- 200 OK:
[
  {
    "user_id": user.id,
    "login": user.login
  }
]

---

#### GET /{user_id}

Returns detailed information for a specific user, including their tasks.

**Responses:**
- 200 OK:
{
  "id": user.id,
  "password": user.password,
  "login": user.login,
  "tasks": [
    {
      "id": task.id,
      "title": task.title,
      "description": task.description,
      "status": task.status,
      "owner_id": task.owner_id
    }
  ]
}
- 404 Not Found: {}

---

### Task Endpoints

#### POST /tasks/new

Creates a new task.

**Request Body:**
{
  "title": "Task Title",
  "description": "Task description"
}

**Responses:**
- 201 Created:
{
  "id": task.id,
  "title": task.title,
  "description": task.description,
  "status": task.status,
  "owner_id": task.owner_id
}
- 400 Bad Request:
{
  "error": "Title and description are required!"
}

---

#### POST /tasks/<int:task_id>/edit

Updates an existing task.

**Request Body:**
{
  "title": "Updated Title",
  "description": "Updated description"
}

**Responses:**
- 200 OK:
{
  "message": "Task updated successfully!"
}
- 403 Forbidden:
{
  "error": "You are not authorized to edit this task"
}

---

#### POST /tasks/<int:task_id>/update_status

Updates the status of a task.

**Request Body:**
{
  "status": 0 | 1 | 2
}

**Responses:**
- 200 OK:
{
  "message": "Task status updated successfully!",
  "status": task.status
}
- 400 Bad Request:
{
  "error": "Invalid status code"
}

---

#### POST /tasks/<int:task_id>/delete

Deletes a task.

**Responses:**
- 200 OK:
{
  "message": "Task deleted successfully!"
}
- 403 Forbidden:
{
  "error": "You are not authorized to delete this task"
}
- 404 Not Found:
{
  "error": "Task not found"
}

---

#### POST /tasks/<int:task_id>/assign

Assigns a task to a user.

**Request Body:**
{
  "user_id": 1
}

**Responses:**
- 200 OK:
{
  "message": "Task assigned to user successfully!"
}
- 409 Conflict:
{
  "warning": "Task is already assigned to this user"
}
- 404 Not Found:
{
  "error": "User not found"
}

---

#### POST /tasks/<int:task_id>/deassign

Deassigns a task from a user.

**Request Body:**
{
  "user_id": 1
}

**Responses:**
- 200 OK:
{
  "message": "Task deassigned from user successfully!"
}
- 409 Conflict:
{
  "warning": "Task is not assigned to this user"
}
- 404 Not Found:
{
  "error": "User not found"
}

---

#### GET /tasks

Returns a list of all tasks.

**Responses:**
- 200 OK:
[
  {
    "id": task.id,
    "title": task.title,
    "description": task.description,
    "status": task.status,
    "owner_id": task.owner_id
  }
]

---

#### GET /tasks/<int:task_id>

Returns detailed information for a specific task, including assigned users.

**Responses:**
- 200 OK:
{
  "id": task.id,
  "title": task.title,
  "description": task.description,
  "status": task.status,
  "owner_id": task.owner_id,
  "assigned_users": [
    {
      "id": user.id,
      "login": user.login
    }
  ]
}
- 404 Not Found:
{
  "error": "Task not found"
}
