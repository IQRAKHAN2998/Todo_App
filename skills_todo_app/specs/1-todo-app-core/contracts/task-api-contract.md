# Task API Contract

## Overview
This document defines the contract for the task management API within the console Todo application.

## Core Operations

### 1. Add Task
- **Method**: `add_task(title: str, description: str = "") -> int`
- **Purpose**: Creates a new task with the provided title and description
- **Parameters**:
  - `title` (str, required): The task title (must not be empty)
  - `description` (str, optional): Detailed task information
- **Returns**: `int` - The unique ID of the created task
- **Errors**:
  - Raises exception if title is empty or contains only whitespace

### 2. Get All Tasks
- **Method**: `get_all_tasks() -> List[Task]`
- **Purpose**: Retrieves all tasks in the collection
- **Parameters**: None
- **Returns**: `List[Task]` - List of all Task objects
- **Errors**: None

### 3. Get Task by ID
- **Method**: `get_task_by_id(task_id: int) -> Task`
- **Purpose**: Retrieves a specific task by its ID
- **Parameters**:
  - `task_id` (int, required): The unique identifier of the task
- **Returns**: `Task` - The requested Task object
- **Errors**:
  - Raises exception if task_id does not exist

### 4. Update Task
- **Method**: `update_task(task_id: int, title: str = None, description: str = None) -> bool`
- **Purpose**: Updates the title and/or description of an existing task
- **Parameters**:
  - `task_id` (int, required): The unique identifier of the task
  - `title` (str, optional): New task title (if provided)
  - `description` (str, optional): New task description (if provided)
- **Returns**: `bool` - True if update was successful, False otherwise
- **Errors**:
  - Raises exception if task_id does not exist
  - Raises exception if title is provided but is empty

### 5. Delete Task
- **Method**: `delete_task(task_id: int) -> bool`
- **Purpose**: Removes a task from the collection
- **Parameters**:
  - `task_id` (int, required): The unique identifier of the task
- **Returns**: `bool` - True if deletion was successful, False otherwise
- **Errors**:
  - Raises exception if task_id does not exist

### 6. Mark Task Complete/Incomplete
- **Method**: `mark_task_status(task_id: int, completed: bool) -> bool`
- **Purpose**: Updates the completion status of a task
- **Parameters**:
  - `task_id` (int, required): The unique identifier of the task
  - `completed` (bool, required): True for complete, False for incomplete
- **Returns**: `bool` - True if status update was successful, False otherwise
- **Errors**:
  - Raises exception if task_id does not exist

## Task Model Definition

### Properties
- `id: int` - Unique sequential identifier
- `title: str` - Task title
- `description: str` - Task description (optional)
- `completed: bool` - Completion status (default: False)
- `created: datetime` - Timestamp of creation

## Error Handling
All methods that can fail will raise appropriate exceptions with descriptive messages to be handled by the calling code.