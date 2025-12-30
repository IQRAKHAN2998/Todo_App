"""
Task model for the Todo application
Contains Task entity and TaskList collection class
"""
from datetime import datetime, timedelta
from typing import List, Optional
import json


class Task:
    """Represents a single task in the Todo application."""

    def __init__(self, task_id: int, title: str, description: str = "", completed: bool = False, priority: str = "medium", due_date: Optional[datetime] = None, category: str = "General", recurrence_pattern: Optional[str] = None, next_occurrence: Optional[datetime] = None, reminder_datetime: Optional[datetime] = None):
        """
        Initialize a new Task.

        Args:
            task_id (int): Unique sequential identifier
            title (str): Task title
            description (str): Task description (optional)
            completed (bool): Completion status (default: False)
            priority (str): Task priority level (default: "medium")
            due_date (datetime, optional): Task due date
            category (str): Task category (default: "General")
            recurrence_pattern (str, optional): Recurrence pattern ("daily", "weekly", "monthly", "yearly")
            next_occurrence (datetime, optional): Next occurrence date for recurring tasks
            reminder_datetime (datetime, optional): Reminder datetime for notifications
        """
        if not title or title.strip() == "":
            raise ValueError("Task title cannot be empty")
        if priority not in ["low", "medium", "high"]:
            raise ValueError("Priority must be one of: low, medium, high")
        if recurrence_pattern and recurrence_pattern not in ["daily", "weekly", "monthly", "yearly"]:
            raise ValueError("Recurrence pattern must be one of: daily, weekly, monthly, yearly")

        self.id = task_id
        self.title = title.strip()
        self.description = description.strip()
        self.completed = completed
        self.created = datetime.now()
        self.priority = priority
        self.due_date = due_date
        self.category = category.strip()
        self.recurrence_pattern = recurrence_pattern
        self.next_occurrence = next_occurrence
        self.reminder_datetime = reminder_datetime

    def __str__(self) -> str:
        """String representation of the task."""
        status_marker = "✓" if self.completed else "○"
        priority_marker = {"high": "❗", "medium": "🔸", "low": "🔹"}[self.priority]
        due_date_str = f" (Due: {self.due_date.strftime('%Y-%m-%d')})" if self.due_date else ""
        recurrence_str = f" 🔁 {self.recurrence_pattern}" if self.recurrence_pattern else ""
        next_occurrence_str = f" (Next: {self.next_occurrence.strftime('%Y-%m-%d')})" if self.next_occurrence else ""
        reminder_str = f" ⏰ {self.reminder_datetime.strftime('%Y-%m-%d %H:%M')}" if self.reminder_datetime else ""
        return f"[{status_marker}] {priority_marker} {self.id}. {self.title} [{self.category}]{due_date_str}{recurrence_str}{next_occurrence_str}{reminder_str}\n    {self.description}"

    def __repr__(self) -> str:
        """Developer representation of the task."""
        due_date_str = self.due_date.isoformat() if self.due_date else None
        next_occurrence_str = self.next_occurrence.isoformat() if self.next_occurrence else None
        reminder_str = self.reminder_datetime.isoformat() if self.reminder_datetime else None
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', completed={self.completed}, priority='{self.priority}', due_date={due_date_str}, category='{self.category}', recurrence_pattern='{self.recurrence_pattern}', next_occurrence={next_occurrence_str}, reminder_datetime={reminder_str})"

    def to_dict(self) -> dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "created": self.created.isoformat(),
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "category": self.category,
            "recurrence_pattern": self.recurrence_pattern,
            "next_occurrence": self.next_occurrence.isoformat() if self.next_occurrence else None,
            "reminder_datetime": self.reminder_datetime.isoformat() if self.reminder_datetime else None
        }


class TaskList:
    """Collection of Task entities with CRUD operations."""

    def __init__(self):
        """Initialize an empty task collection."""
        self._tasks = {}  # Dictionary to store tasks by ID
        self._next_id = 1  # Counter for generating unique IDs

    def add_task(self, title: str, description: str = "", priority: str = "medium", due_date: Optional[datetime] = None, category: str = "General", recurrence_pattern: Optional[str] = None, next_occurrence: Optional[datetime] = None, reminder_datetime: Optional[datetime] = None) -> int:
        """
        Add a new task to the collection.

        Args:
            title (str): Task title
            description (str): Task description (optional)
            priority (str): Task priority level (default: "medium")
            due_date (datetime, optional): Task due date
            category (str): Task category (default: "General")
            recurrence_pattern (str, optional): Recurrence pattern ("daily", "weekly", "monthly", "yearly")
            next_occurrence (datetime, optional): Next occurrence date for recurring tasks
            reminder_datetime (datetime, optional): Reminder datetime for notifications

        Returns:
            int: The unique ID of the created task
        """
        if not title or title.strip() == "":
            raise ValueError("Task title cannot be empty")
        if priority not in ["low", "medium", "high"]:
            raise ValueError("Priority must be one of: low, medium, high")
        if recurrence_pattern and recurrence_pattern not in ["daily", "weekly", "monthly", "yearly"]:
            raise ValueError("Recurrence pattern must be one of: daily, weekly, monthly, yearly")

        task_id = self._next_id
        task = Task(task_id, title, description, completed=False, priority=priority, due_date=due_date, category=category, recurrence_pattern=recurrence_pattern, next_occurrence=next_occurrence, reminder_datetime=reminder_datetime)
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

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, due_date: Optional[datetime] = None, category: Optional[str] = None, recurrence_pattern: Optional[str] = None, next_occurrence: Optional[datetime] = None, reminder_datetime: Optional[datetime] = None) -> bool:
        """
        Update an existing task's title and/or description.

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
            ValueError: If title is provided but is empty, or priority/recurrence pattern is invalid
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

        if priority is not None:
            if priority not in ["low", "medium", "high"]:
                raise ValueError("Priority must be one of: low, medium, high")
            task.priority = priority

        if due_date is not None:
            task.due_date = due_date

        if category is not None:
            task.category = category.strip()

        if recurrence_pattern is not None:
            if recurrence_pattern not in ["daily", "weekly", "monthly", "yearly"] and recurrence_pattern != "":
                raise ValueError("Recurrence pattern must be one of: daily, weekly, monthly, yearly, or empty string to remove")
            task.recurrence_pattern = recurrence_pattern if recurrence_pattern != "" else None

        if next_occurrence is not None:
            task.next_occurrence = next_occurrence

        if reminder_datetime is not None:
            task.reminder_datetime = reminder_datetime

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

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """
        Get tasks filtered by completion status.

        Args:
            completed (bool): True for completed tasks, False for pending tasks

        Returns:
            List[Task]: List of tasks with the specified completion status
        """
        return [task for task in self._tasks.values() if task.completed == completed]

    def search_tasks(self, query: str) -> List[Task]:
        """
        Search tasks by title or description.

        Args:
            query (str): Search query string

        Returns:
            List[Task]: List of tasks that match the query
        """
        query_lower = query.lower()
        return [task for task in self._tasks.values()
                if query_lower in task.title.lower() or query_lower in task.description.lower()]

    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """
        Get tasks filtered by priority level.

        Args:
            priority (str): Priority level ("low", "medium", "high")

        Returns:
            List[Task]: List of tasks with the specified priority
        """
        return [task for task in self._tasks.values() if task.priority == priority]

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """
        Get tasks filtered by category.

        Args:
            category (str): Category name

        Returns:
            List[Task]: List of tasks in the specified category
        """
        return [task for task in self._tasks.values() if task.category.lower() == category.lower()]

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get tasks that are overdue (due date is in the past and not completed).

        Returns:
            List[Task]: List of overdue tasks
        """
        now = datetime.now()
        return [task for task in self._tasks.values()
                if task.due_date and task.due_date < now and not task.completed]

    def get_tasks_by_due_date_range(self, start_date: datetime, end_date: datetime) -> List[Task]:
        """
        Get tasks within a specific due date range.

        Args:
            start_date (datetime): Start date of the range
            end_date (datetime): End date of the range

        Returns:
            List[Task]: List of tasks within the due date range
        """
        return [task for task in self._tasks.values()
                if task.due_date and start_date <= task.due_date <= end_date]

    def save_to_file(self, filename: str) -> bool:
        """
        Save all tasks to a JSON file.

        Args:
            filename (str): Path to the file to save tasks

        Returns:
            bool: True if save was successful, False otherwise
        """
        try:
            import json
            from datetime import datetime
            tasks_data = []
            for task in self._tasks.values():
                task_dict = task.to_dict()
                # Convert datetime objects to ISO format strings for JSON serialization
                task_dict['created'] = task.created.isoformat()
                if task.due_date:
                    task_dict['due_date'] = task.due_date.isoformat()
                tasks_data.append(task_dict)

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(tasks_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving tasks to file: {e}")
            return False

    def load_from_file(self, filename: str) -> bool:
        """
        Load tasks from a JSON file.

        Args:
            filename (str): Path to the file to load tasks from

        Returns:
            bool: True if load was successful, False otherwise
        """
        try:
            import json
            from datetime import datetime
            with open(filename, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)

            # Clear existing tasks
            self._tasks = {}
            max_id = 0

            for task_data in tasks_data:
                task_id = task_data['id']
                title = task_data['title']
                description = task_data['description']
                completed = task_data['completed']
                priority = task_data.get('priority', 'medium')
                category = task_data.get('category', 'General')

                # Parse datetime strings
                created = datetime.fromisoformat(task_data['created'].replace('Z', '+00:00'))
                due_date = None
                if task_data.get('due_date'):
                    due_date = datetime.fromisoformat(task_data['due_date'].replace('Z', '+00:00'))

                # Parse recurrence and reminder datetimes
                recurrence_pattern = task_data.get('recurrence_pattern')
                next_occurrence = None
                if task_data.get('next_occurrence'):
                    next_occurrence = datetime.fromisoformat(task_data['next_occurrence'].replace('Z', '+00:00'))

                reminder_datetime = None
                if task_data.get('reminder_datetime'):
                    reminder_datetime = datetime.fromisoformat(task_data['reminder_datetime'].replace('Z', '+00:00'))

                # Create task with loaded data
                task = Task(task_id, title, description, completed, priority, due_date, category, recurrence_pattern, next_occurrence, reminder_datetime)
                task.created = created  # Override the created time with loaded value
                self._tasks[task_id] = task
                max_id = max(max_id, task_id)

            # Set the next ID to be one more than the highest loaded ID
            self._next_id = max_id + 1
            return True
        except FileNotFoundError:
            # If file doesn't exist, that's okay - we'll start with an empty task list
            return True
        except Exception as e:
            print(f"Error loading tasks from file: {e}")
            return False

    def get_statistics(self) -> dict:
        """
        Get task statistics and productivity metrics.

        Returns:
            dict: Dictionary containing various task statistics
        """
        all_tasks = list(self._tasks.values())
        total_tasks = len(all_tasks)
        completed_tasks = len([task for task in all_tasks if task.completed])
        pending_tasks = total_tasks - completed_tasks

        # Calculate completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

        # Count by priority
        priority_counts = {"high": 0, "medium": 0, "low": 0}
        for task in all_tasks:
            priority_counts[task.priority] += 1

        # Count by category
        category_counts = {}
        for task in all_tasks:
            category_counts[task.category] = category_counts.get(task.category, 0) + 1

        # Count overdue tasks
        overdue_tasks = len(self.get_overdue_tasks())

        # Count recurring tasks
        recurring_tasks = len([task for task in all_tasks if task.recurrence_pattern])

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "completion_rate": round(completion_rate, 2),
            "priority_breakdown": priority_counts,
            "category_breakdown": category_counts,
            "overdue_tasks": overdue_tasks,
            "recurring_tasks": recurring_tasks
        }

    def get_recurring_tasks(self) -> List[Task]:
        """
        Get all recurring tasks.

        Returns:
            List[Task]: List of recurring tasks
        """
        return [task for task in self._tasks.values() if task.recurrence_pattern]

    def process_recurring_tasks(self) -> int:
        """
        Process recurring tasks and create new instances when needed.

        Returns:
            int: Number of new tasks created
        """
        from datetime import timedelta
        now = datetime.now()
        new_tasks_created = 0

        # Find completed recurring tasks that should generate new ones
        for task in list(self._tasks.values()):  # Use list() to avoid modification during iteration
            if (task.recurrence_pattern and task.completed and
                task.next_occurrence and task.next_occurrence <= now):

                # Calculate next occurrence date based on pattern
                next_occurrence = self._calculate_next_occurrence(task.next_occurrence, task.recurrence_pattern)

                # Create a new task with the same properties but reset completion status
                new_task_id = self._next_id
                new_task = Task(
                    task_id=new_task_id,
                    title=task.title,
                    description=task.description,
                    priority=task.priority,
                    due_date=task.due_date,  # Original due date
                    category=task.category,
                    recurrence_pattern=task.recurrence_pattern,
                    next_occurrence=next_occurrence
                )

                # If the original task had a due date, adjust the new task's due date by the same interval
                if task.due_date:
                    original_interval = task.due_date - task.created
                    new_task.due_date = new_task.created + original_interval

                self._tasks[new_task_id] = new_task
                self._next_id += 1
                new_tasks_created += 1

                # Update the original task's next occurrence
                task.next_occurrence = next_occurrence
                task.completed = False  # Reset completion status for the original task

        return new_tasks_created

    def _calculate_next_occurrence(self, current_date: datetime, pattern: str) -> datetime:
        """
        Calculate the next occurrence date based on the recurrence pattern.

        Args:
            current_date (datetime): Current occurrence date
            pattern (str): Recurrence pattern ("daily", "weekly", "monthly", "yearly")

        Returns:
            datetime: Next occurrence date
        """
        if pattern == "daily":
            return current_date + timedelta(days=1)
        elif pattern == "weekly":
            return current_date + timedelta(weeks=1)
        elif pattern == "monthly":
            # For monthly, add one month (approximately 30 days)
            # This is a simplified approach - could be enhanced to handle month boundaries
            try:
                next_month = current_date.month + 1
                next_year = current_date.year
                if next_month > 12:
                    next_month = 1
                    next_year += 1

                # Handle day overflow (e.g., Jan 31 + 1 month should become Feb 28/29)
                import calendar
                max_day = calendar.monthrange(next_year, next_month)[1]
                day = min(current_date.day, max_day)

                return current_date.replace(year=next_year, month=next_month, day=day)
            except ValueError:
                # Fallback for edge cases
                return current_date + timedelta(days=30)
        elif pattern == "yearly":
            try:
                return current_date.replace(year=current_date.year + 1)
            except ValueError:
                # Handle leap year edge case (Feb 29)
                return current_date.replace(year=current_date.year + 1, month=2, day=28)
        else:
            return current_date  # Should not happen if validation is working properly

    def get_upcoming_reminders(self, within_minutes: int = 60) -> List[Task]:
        """
        Get tasks with reminders that are upcoming within the specified time window.

        Args:
            within_minutes (int): Time window in minutes to check for upcoming reminders

        Returns:
            List[Task]: List of tasks with upcoming reminders
        """
        now = datetime.now()
        future_time = now + timedelta(minutes=within_minutes)

        return [
            task for task in self._tasks.values()
            if task.reminder_datetime and
            now < task.reminder_datetime <= future_time and
            not task.completed
        ]