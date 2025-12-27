# Sub-Agents for Python In-Memory Console Todo App

This document defines the sub-agents for the Python in-memory console Todo application.

## 1. InputAgent
- **Responsibility**: Handle user input validation and command parsing for the console interface
- **Skills Used**: validate_input (from skills), add_task, update_task, delete_task, mark_task_complete

## 2. TaskManagerAgent
- **Responsibility**: Manage the core task operations including adding, updating, deleting, and marking tasks as complete
- **Skills Used**: add_task, update_task, delete_task, mark_task_complete

## 3. StorageAgent
- **Responsibility**: Handle in-memory storage operations for tasks including initialization and data persistence
- **Skills Used**: manage_storage, view_tasks

## 4. DisplayAgent
- **Responsibility**: Format and display task information to the console for user interaction
- **Skills Used**: view_tasks, add_task, mark_task_complete

These agents are designed to be minimal and aligned with the in-memory console application, with each agent having a clear responsibility and using the previously defined skills.