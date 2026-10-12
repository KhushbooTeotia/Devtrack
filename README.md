# DevTrack — Engineering Issue Tracker API

## 1. Project Overview

DevTrack is a beginner-friendly Django backend API for tracking engineering issues. It allows engineers to create reporters, report bugs, assign priorities, update issue statuses, and retrieve issues using HTTP requests.

This project uses Python object-oriented programming (OOP) and JSON files for data storage, as required by the assignment.

## 2. Technologies Used

- Python
- Django 5.2
- JSON for file-based data storage
- Postman for API testing
- Git and GitHub for version control

## 3. Features

- Create and retrieve reporters.
- Create and retrieve engineering issues.
- Find reporters and issues by ID.
- Filter issues by status.
- Validate reporter details, issue titles, priorities, and statuses.
- Associate each issue with an existing reporter.
- Use inheritance and method overriding for priority-specific descriptions.
- Persist records in `reporters.json` and `issues.json`.

## 4. Project Structure

```text
devtrack-project/
├── manage.py
├── requirements.txt
├── README.md
├── reporters.json
├── issues.json
├── devtrack/
│   ├── settings.py
│   └── urls.py
├── issues/
│   ├── models.py
│   ├── views.py
│   └── urls.py
└── screenshots/
    ├── issue-success.png
    └── issue-validation-error.png
```

## 5. Setup and Installation

### Prerequisites

- Python installed on your computer
- Visual Studio Code or another code editor
- Postman for testing API endpoints

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd devtrack-project
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL of your GitHub repository.

### Step 2: Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Initialize the JSON files

Ensure `reporters.json` and `issues.json` exist in the project root. Each file should initially contain:

```json
[]
```

### Step 5: Run Django checks

```powershell
python manage.py check
```

### Step 6: Apply Django migrations

```powershell
python manage.py migrate
```

### Step 7: Start the development server

```powershell
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/`

## 6. API Endpoints

All endpoints use the base URL `http://127.0.0.1:8000`.

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/reporters/` | Create a reporter |
| GET | `/api/reporters/` | Retrieve all reporters |
| GET | `/api/reporters/?id=1` | Retrieve a reporter by ID |
| POST | `/api/issues/` | Create an issue |
| GET | `/api/issues/` | Retrieve all issues |
| GET | `/api/issues/?id=1` | Retrieve an issue by ID |
| GET | `/api/issues/?status=open` | Filter issues by status |

### Example: Create a reporter

**Request**

`POST /api/reporters/`

```json
{
  "id": 1,
  "name": "Khushboo",
  "email": "khushboo@example.com",
  "team": "backend"
}
```

**Expected status:** `201 Created`

### Example: Create a critical issue

**Request**

`POST /api/issues/`

```json
{
  "id": 1,
  "title": "Login button not working on mobile",
  "description": "Users on iOS 17 cannot tap the login button",
  "status": "open",
  "priority": "critical",
  "reporter_id": 1
}
```

**Expected status:** `201 Created`

The response includes a priority-specific message:

```json
{
  "message": "[URGENT] Login button not working on mobile — needs immediate attention"
}
```

The complete response also contains the issue fields and generated timestamp.

## 7. Allowed Values

### Issue statuses

- `open`
- `in_progress`
- `resolved`
- `closed`

### Issue priorities

- `low`
- `medium`
- `high`
- `critical`

## 8. Object-Oriented Design

The project implements the following OOP concepts:

- **Abstraction:** `BaseEntity` is an abstract class that requires subclasses to implement `validate()`.
- **Inheritance:** `Reporter` and `Issue` inherit from `BaseEntity`.
- **Method overriding:** `CriticalIssue` and `LowPriorityIssue` override `describe()` to provide priority-specific messages.
- **Encapsulation of behavior:** Each class contains its own data and validation behavior.
- **Serialization:** `to_dict()` converts an object's attributes into a dictionary for JSON responses.

## 9. Design Decision

I chose JSON files for storage because the assignment specifically requires file-based persistence instead of storing application records in a database.

I also created a shared `BaseEntity` class to avoid duplicating common behavior and used specialized issue subclasses to demonstrate inheritance and method overriding.

This approach keeps the project simple and demonstrates the required OOP concepts. JSON file storage is suitable for this learning assignment but is not intended for concurrent, production-scale use.

## 10. Error Handling

The API uses the following HTTP status codes:

- `200 OK` — successful retrieval.
- `201 Created` — successful record creation.
- `400 Bad Request` — invalid input or validation failure.
- `404 Not Found` — requested record or referenced reporter does not exist.
- `405 Method Not Allowed` — unsupported HTTP method.

## 11. API Testing with Postman

The endpoints were tested using Postman.

### Successful Request

Add a screenshot showing a successful issue creation request and its `201 Created` response.

![Successful issue creation](screenshots/issue-success.png)

### Validation Failure

Add a screenshot showing an invalid issue creation request and its `400 Bad Request` response.

![Issue validation failure](screenshots/issue-validation-error.png)

## 12. Limitations

- Data is stored in JSON files rather than a relational database.
- JSON file storage does not provide robust concurrent-write protection.
- Authentication and authorization are not implemented.
- This is a learning project and is not intended for production deployment.
