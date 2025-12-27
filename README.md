# Todo App

A console-based Todo application with in-memory storage that allows users to manage tasks through a menu interface. The application supports the five core task operations: Add, Delete, Update, View, and Mark Complete/Incomplete.

## Features

- Add new tasks with title and description
- View all tasks with their completion status
- Update existing task information
- Delete tasks from the list
- Mark tasks as complete/incomplete
- In-memory storage with unique sequential IDs

## Requirements

- Python 3.13 or higher

## Installation

1. Clone or download the repository
2. Ensure Python 3.13+ is installed (`python --version`)
3. No additional dependencies required

## Usage

Run the application:
```bash
python main.py
```

The application will start with a menu interface that allows you to:
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete/Incomplete
6. Exit

## Testing

Run the unit tests:
```bash
python -m pytest tests/unit/
```

Run the integration tests:
```bash
python -m pytest tests/integration/
```

Run the contract tests:
```bash
python -m pytest tests/contract/
```

Run all tests:
```bash
python -m pytest
```

Run the performance test:
```bash
python tests/performance_test.py
```

## Project Structure

```
src/
├── models/
│   └── task.py          # Task entity and TaskList collection
├── services/
│   └── todo_service.py  # Business logic for task operations
└── cli/
    └── menu.py          # Console menu interface

tests/
├── unit/
├── integration/
└── contract/
```

## Development

- Source code is located in the `src/` directory
- Models in `src/models/`
- Services in `src/services/`
- CLI interface in `src/cli/`
- Tests in `tests/` directory