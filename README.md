# Smart Home Automation Backend

A FastAPI backend for a smart home automation and energy monitoring system.

The backend processes user commands and converts them into structured device actions for smart home devices such as lights, fans, and air conditioners. It also provides API endpoints that can be used by a frontend dashboard for device control, automation, and monitoring.

## Features

* REST API built with FastAPI
* Smart device action processing
* Support for lights, fans, and air conditioners
* Converts user commands into structured device actions
* Device action tracking
* Voice command processing
* API endpoints for retrieving recent actions
* Backend support for smart home automation workflows
* Designed to integrate with a React-based smart home dashboard

## Tech Stack

* Python
* FastAPI
* Uvicorn
* REST APIs

## Project Architecture

```text
User
  │
  │ Text / Voice Command
  ▼
Smart Home Dashboard
  │
  │ API Request
  ▼
FastAPI Backend
  │
  │ Command Processing
  ▼
Decision Logic
  │
  ▼
Structured Device Actions
  │
  ├── Lights
  ├── Fans
  └── Air Conditioners
```

## Project Structure

```text
smart-home-backend/
├── app.py
├── llm_agent.py
├── tests/
├── requirements.txt
└── README.md
```

> The project structure may contain additional development and configuration files.

## Installation

Clone the repository:

```bash
git clone https://github.com/betty1-3/smart-home-backend.git
cd smart-home-backend
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

The API will typically be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive API documentation.

Once the server is running, visit:

```text
http://127.0.0.1:8000/docs
```

## Core API Endpoints

### Process a Command

```text
POST /decide
```

Processes a user command and determines the appropriate smart device actions.

### Process a Voice Command

```text
POST /voice-decide
```

Processes voice-based smart home commands and converts them into structured actions.

### Retrieve Device Actions

```text
GET /actions
```

Retrieves generated device actions.

### Retrieve Recent Actions

```text
GET /last-actions
```

Retrieves the most recently generated smart home actions.

## Example Workflow

```text
User Command:
"Turn on the living room light and switch off the fan."

        ↓

Backend Processing

        ↓

Structured Actions

        ↓

Light → ON
Fan   → OFF
```

## Frontend Integration

This backend is designed to work with a smart home dashboard frontend.

The frontend can send user commands and retrieve device actions through the REST API.

```text
Smart Home Dashboard
        ↓
FastAPI Backend
        ↓
Command Processing
        ↓
Device Actions
```

## Related Project

This backend is part of a larger Smart Home Automation and Energy Monitoring project.

The frontend dashboard provides interfaces for:

* Device control
* Sensor monitoring
* Energy monitoring
* Automation rules
* Smart home statistics

## Future Improvements

* Improve AI-based command understanding
* Support more smart home devices
* Improve automation rule processing
* Add authentication and authorization
* Add persistent device state storage
* Add real IoT device integration
* Improve voice command processing
* Add automated API tests
* Add structured logging
* Improve CORS configuration
* Add Docker support

## Development Notes

This project is currently under active development.

Some components and integrations may still be prototypes or use simplified logic while the full smart home system is being developed.

## Author

GitHub: [@betty1-3](https://github.com/betty1-3)
