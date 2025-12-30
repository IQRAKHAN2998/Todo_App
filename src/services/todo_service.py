"""
TodoService for the Todo application
Business logic for task operations
"""
from datetime import datetime
from typing import List, Optional
from src.models.task import Task, TaskList


class TodoService:
    """Business logic layer for task operations."""

    def __init__(self):
        """Initialize the TodoService with a TaskList."""
        self.task_list = TaskList()

    def add_task(self, title: str, description: str = "", priority: str = "medium", due_date: Optional[datetime] = None, category: str = "General", recurrence_pattern: Optional[str] = None, next_occurrence: Optional[datetime] = None, reminder_datetime: Optional[datetime] = None) -> int:
        """
        Create a new task with the provided title and description.

        Args:
            title (str): The task title (must not be empty)
            description (str, optional): Detailed task information
            priority (str): Task priority level (default: "medium")
            due_date (datetime, optional): Task due date
            category (str): Task category (default: "General")
            recurrence_pattern (str, optional): Recurrence pattern ("daily", "weekly", "monthly", "yearly")
            next_occurrence (datetime, optional): Next occurrence date for recurring tasks
            reminder_datetime (datetime, optional): Reminder datetime for notifications

        Returns:
            int: The unique ID of the created task

        Raises:
            ValueError: If title is empty or contains only whitespace
        """
        return self.task_list.add_task(title, description, priority, due_date, category, recurrence_pattern, next_occurrence, reminder_datetime)

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

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, due_date: Optional[datetime] = None, category: Optional[str] = None, recurrence_pattern: Optional[str] = None, next_occurrence: Optional[datetime] = None, reminder_datetime: Optional[datetime] = None) -> bool:
        """
        Update the title, description, priority, due date, and/or category of an existing task.

        Args:
            task_id (int): The unique identifier of the task
            title (str, optional): New task title (if provided)
            description (str, optional): New task description (if provided)
            priority (str, optional): New task priority (if provided)
            due_date (datetime, optional): New task due date (if provided)
            category (str, optional): New task category (if provided)
            recurrence_pattern (str, optional): New recurrence pattern (if provided)
            next_occurrence (datetime, optional): New next occurrence date (if provided)
            reminder_datetime (datetime, optional): New reminder datetime (if provided)

        Returns:
            bool: True if update was successful, False otherwise

        Raises:
            KeyError: If task_id does not exist
            ValueError: If title is provided but is empty, or priority is invalid
        """
        return self.task_list.update_task(task_id, title, description, priority, due_date, category, recurrence_pattern, next_occurrence, reminder_datetime)

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

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """
        Get tasks filtered by completion status.

        Args:
            completed (bool): True for completed tasks, False for pending tasks

        Returns:
            List[Task]: List of tasks with the specified completion status
        """
        return self.task_list.get_tasks_by_status(completed)

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title or description.

        Args:
            query (str): Search query string

        Returns:
            List[Task]: List of tasks that match the query
        """
        return self.task_list.search_tasks(query)

    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """
        Get tasks filtered by priority level.

        Args:
            priority (str): Priority level ("low", "medium", "high")

        Returns:
            List[Task]: List of tasks with the specified priority
        """
        return self.task_list.get_tasks_by_priority(priority)

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """
        Get tasks filtered by category.

        Args:
            category (str): Category name

        Returns:
            List[Task]: List of tasks in the specified category
        """
        return self.task_list.get_tasks_by_category(category)

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get tasks that are overdue (due date is in the past and not completed).

        Returns:
            List[Task]: List of overdue tasks
        """
        return self.task_list.get_overdue_tasks()

    def get_tasks_by_due_date_range(self, start_date: datetime, end_date: datetime) -> List[Task]:
        """
        Get tasks within a specific due date range.

        Args:
            start_date (datetime): Start date of the range
            end_date (datetime): End date of the range

        Returns:
            List[Task]: List of tasks within the due date range
        """
        return self.task_list.get_tasks_by_due_date_range(start_date, end_date)

    def save_to_file(self, filename: str) -> bool:
        """
        Save all tasks to a JSON file.

        Args:
            filename (str): Path to the file to save tasks

        Returns:
            bool: True if save was successful, False otherwise
        """
        return self.task_list.save_to_file(filename)

    def load_from_file(self, filename: str) -> bool:
        """
        Load tasks from a JSON file.

        Args:
            filename (str): Path to the file to load tasks from

        Returns:
            bool: True if load was successful, False otherwise
        """
        return self.task_list.load_from_file(filename)

    def get_statistics(self) -> dict:
        """
        Get task statistics and productivity metrics.

        Returns:
            dict: Dictionary containing various task statistics
        """
        return self.task_list.get_statistics()

    def get_recurring_tasks(self) -> List[Task]:
        """
        Get all recurring tasks.

        Returns:
            List[Task]: List of recurring tasks
        """
        return self.task_list.get_recurring_tasks()

    def process_recurring_tasks(self) -> int:
        """
        Process recurring tasks and create new instances when needed.

        Returns:
            int: Number of new tasks created
        """
        return self.task_list.process_recurring_tasks()

    def get_upcoming_reminders(self, within_minutes: int = 60) -> List[Task]:
        """
        Get tasks with reminders that are upcoming within the specified time window.

        Args:
            within_minutes (int): Time window in minutes to check for upcoming reminders

        Returns:
            List[Task]: List of tasks with upcoming reminders
        """
        return self.task_list.get_upcoming_reminders(within_minutes)