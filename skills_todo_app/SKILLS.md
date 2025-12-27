# Skills Definition for Python In-Memory Console Todo App

This document defines the reusable skills for the Python in-memory console Todo application.

## 1. add_task
- **Responsibility**: Add a new task to the in-memory task list with a unique ID and initial status
- **Inputs**: task_description (string), task_id (optional integer)
- **Outputs**: success message with task ID, or error message if validation fails

## 2. delete_task
- **Responsibility**: Remove a task from the in-memory task list by its ID
- **Inputs**: task_id (integer)
- **Outputs**: success message confirming deletion, or error message if task not found

## 3. update_task
- **Responsibility**: Modify an existing task's description or other properties
- **Inputs**: task_id (integer), new_description (string), other_updates (optional dictionary)
- **Outputs**: success message confirming update, or error message if task not found/invalid

## 4. view_tasks
- **Responsibility**: Display all tasks in the in-memory storage with their status and details
- **Inputs**: filter_options (optional dictionary for filtering by status/completion)
- **Outputs**: formatted list of tasks with ID, description, and completion status

## 5. mark_task_complete
- **Responsibility**: Mark a task as complete or incomplete
- **Inputs**: task_id (integer), is_complete (boolean - True for complete, False for incomplete)
- **Outputs**: success message with new status, or error message if task not found

These skills are designed for reuse across different phases of the application development and provide a clean separation of concerns for the Todo application functionality.