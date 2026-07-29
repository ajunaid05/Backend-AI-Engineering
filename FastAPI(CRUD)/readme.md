# FastAPI CRUD API

Backend AI Engineering – Assignment 1

A simple **Task Management CRUD API** built with **FastAPI**. This project demonstrates the implementation of RESTful CRUD operations, request validation, exception handling, and automatically generated API documentation using **Swagger UI (OpenAPI)**.

---

## Features

* Create a new task
* Retrieve all tasks
* Retrieve a task by ID
* Update an existing task
* Delete a task
* Request validation using Pydantic
* Custom exception handling
* Interactive API documentation with Swagger UI

---

## Tech Stack

* Python 3
* FastAPI
* Pydantic
* Uvicorn

---

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── Images/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/ajunaid05/Backend-AI-Engineering.git
cd Backend-AI-Engineering
cd "FastAPI(CRUD)"
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Run the API

Start the development server using:

```bash
uvicorn main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

---

## API Documentation

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

| Method | Endpoint      | Description             |
| ------ | ------------- | ----------------------- |
| GET    | `/`           | API information         |
| GET    | `/health`     | Health check            |
| GET    | `/tasks`      | Retrieve all tasks      |
| GET    | `/tasks/{id}` | Retrieve a task by ID   |
| POST   | `/tasks`      | Create a new task       |
| PUT    | `/tasks/{id}` | Update an existing task |
| DELETE | `/tasks/{id}` | Delete a task           |

---

## Example API Call

Create a new task using `curl`:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
```

### Example Output

```http
HTTP/1.1 201 Created
date: Wed, 29 Jul 2026 13:57:55 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

---

## HTTP Status Codes

| Status Code         | Description                          |
| ------------------- | ------------------------------------ |
| **200 OK**          | Request completed successfully       |
| **201 Created**     | Resource created successfully        |
| **204 No Content**  | Resource deleted successfully        |
| **400 Bad Request** | Invalid request or validation failed |
| **404 Not Found**   | Requested task was not found         |

---

## Learning Outcomes

This project demonstrates:

* RESTful API development with FastAPI
* CRUD operations (Create, Read, Update, Delete)
* Request validation using Pydantic
* Exception handling using `HTTPException`
* Custom validation error handling
* Proper use of HTTP status codes
* Automatic API documentation with OpenAPI
* Interactive API testing using Swagger UI

---


## Screenshots

### Swagger UI

All API endpoints generated automatically by FastAPI.

![Swagger UI](Images/image.png)

---

### Create Task (POST)

Creating a new task using Swagger UI.

![POST Request](Images/images-1.png)
![POST Response](Images/images-2.png)

---

### Retrieve Tasks (GET)

Listing all available tasks after creating a new one.

![GET Tasks](Images/image-3.png)
![GET Response](Images/image-4.png)

---

### Update Task (PUT)

Updating an existing task and marking it as completed.

![PUT Task](Images/image-5.png)
![PUT Response](Images/image-6.png)

---

### Delete Task (DELETE)

Deleting a task successfully.

![DELETE Task](Images/image-7.png)
![DELETE Response](Images/image-8.png)
---

### Verify Deletion (GET)

Confirming the task has been removed.

![DELETE Verification](Images/image-9.png)

## Example API Call

Create a new task using `curl`:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
```

##curl -i Example with output

(venv) D:\FlyRank Tasks\Backend AI Engineering\FastAPI(CRUD)>curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"Buy milk\"}"
HTTP/1.1 201 Created
date: Wed, 29 Jul 2026 13:57:55 GMT
server: uvicorn
content-length: 40
content-type: application/json

{"id":4,"title":"Buy milk","done":false}

## Author

**Ahmad Junaid**

Backend AI Engineering – Assignment 1

COMSATS University Islamabad