"""
TodoService for the Todo application
Business logic for task operations
"""
from typing import List, Optional
from src.models.task import Task, TaskList


class TodoService:
    """Business logic layer for task operations."""

    def __init__(self):
        """Initialize the TodoService with a TaskList."""
        self.task_list = TaskList()

    def add_task(self, title: str, description: str = "") -> int:
        """
        Create a new task with the provided title and description.

        Args:
            title (str): The task title (must not be empty)
            description (str, optional): Detailed task information

        Returns:
            int: The unique ID of the created task

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        return self.task_list.add_task(title, description)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the collection.

        Returns:
            List[Task]: List of all Task objects
        """
        return self.task_list.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> Task:
        """
        Retrieve a specific task by its ID.

        Args:
            task_id (int): The unique identifier of the task

        Returns:
            Task: The requested Task object

        Raises:
            KeyError: If task_id does not exist
        """
        return self.task_list.get_task_by_id(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """
        Update the title and/or description of an existing task.

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
        return self.task_list.update_task(task_id, title, description)

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
        return self.task_list.delete_task(task_id)

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
        return self.task_list.mark_task_status(task_id, completed)

    def get_next_task_id(self) -> int:
        """
        Get the next available ID for a new task.

        Returns:
            int: The next available ID
        """
        return self.task_list.get_next_id()