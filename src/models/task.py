"""
Task model for the Todo application
Contains Task entity and TaskList collection class
"""
from datetime import datetime
from typing import List, Optional


class Task:
    """Represents a single task in the Todo application."""

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False):
        """
        Initialize a new Task.

        Args:
            task_id (int): Unique sequential identifier
            title (str): Task title
            description (str): Task description (optional)
            completed (bool): Completion status (default: False)
        """
        if not title or title.strip() == "":
            raise ValueError("Task title cannot be empty")

        self.id = task_id
        self.title = title.strip()
        self.description = description.strip()
        self.completed = completed
        self.created = datetime.now()

    def __str__(self) -> str:
        """String representation of the task."""
        status_marker = "✓" if self.completed else "○"
        return f"[{status_marker}] {self.id}. {self.title} - {self.description}"

    def __repr__(self) -> str:
        """Developer representation of the task."""
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed})"

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created": self.created.isoformat()
        }


class TaskList:
    """Collection of Task entities with CRUD operations."""

    def __init__(self):
        """Initialize an empty task collection."""
        self._tasks = {}  # Dictionary to store tasks by ID
        self._next_id = 1  # Counter for generating unique IDs

    def add_task(self, title: str, description: str = "") -> int:
        """
        Add a new task to the collection.

        Args:
            title (str): Task title
            description (str): Task description (optional)

        Returns:
            int: The unique ID of the created task
        """
        if not title or title.strip() == "":
            raise ValueError("Task title cannot be empty")

        task_id = self._next_id
        task = Task(task_id, title, description, completed=False)
        self._tasks[task_id] = task
        self._next_id += 1

        return task_id

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in the collection.

        Returns:
            List[Task]: List of all Task objects
        """
        return list(self._tasks.values())

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Get a specific task by its ID.

        Args:
            task_id (int): The unique identifier of the task

        Returns:
            Task: The requested Task object

        Raises:
            KeyError: If task_id does not exist
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")
        return self._tasks[task_id]

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update an existing task's title and/or description.

        Args:
            task_id (int): The unique identifier of the task
            title (str, optional): New task title (if provided)
            description (str, optional): New task description (if provided)

        Returns:
            bool: True if update was successful, False otherwise

        Raises:
            KeyError: If task_id does not exist
            ValueError: If title is provided but is empty
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")

        task = self._tasks[task_id]

        if title is not None:
            if not title or title.strip() == "":
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip()

        return True

    def delete_task(self, task_id: int) -> bool:
        """
        Remove a task from the collection.

        Args:
            task_id (int): The unique identifier of the task

        Returns:
            bool: True if deletion was successful, False otherwise

        Raises:
            KeyError: If task_id does not exist
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")

        del self._tasks[task_id]
        return True

    def mark_task_status(self, task_id: int, completed: bool) -> bool:
        """
        Update the completion status of a task.

        Args:
            task_id (int): The unique identifier of the task
            completed (bool): True for complete, False for incomplete

        Returns:
            bool: True if status update was successful, False otherwise

        Raises:
            KeyError: If task_id does not exist
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} does not exist")

        task = self._tasks[task_id]
        task.completed = completed
        return True

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new task.

        Returns:
            int: The next available ID
        """
        return self._next_id