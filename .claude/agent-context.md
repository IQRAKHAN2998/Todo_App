# Claude Agent Context for Todo App

## Project Overview
- Console-based Todo application with in-memory storage
- Five core operations: Add, Delete, Update, View, Mark Complete/Incomplete
- Built with Python 3.13+ using object-oriented design

## Key Components
- Task model: Represents individual tasks with ID, title, description, status
- TaskList service: Manages collection of tasks and provides CRUD operations
- Console menu: Interactive CLI interface for user operations

## File Structure
- src/models/task.py: Task entity definition
- src/services/todo_service.py: Business logic for task operations
- src/cli/menu.py: Console interface implementation
- tests/: Unit and integration tests
- main.py: Application entry point

## Important Notes
- All task IDs are auto-incremented integers
- In-memory storage only (no persistence between sessions)
- Input validation required for all user inputs
- Console interface must be user-friendly with clear prompts