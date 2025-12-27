"""
Unit tests for Task model and TaskList collection
"""
import pytest
from datetime import datetime
from src.models.task import Task, TaskList


class TestTask:
    """Test cases for the Task class."""

    def test_task_creation(self):
        """Test creating a new task with valid parameters."""
        task = Task(1, "Test Title", "Test Description", False)
        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False
        assert isinstance(task.created, datetime)

    def test_task_creation_default_values(self):
        """Test creating a task with default values."""
        task = Task(1, "Test Title")
        assert task.id == 1
        assert task.title == "Test Title"
        assert task.description == ""
        assert task.completed is False

    def test_task_title_validation(self):
        """Test that task title cannot be empty."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(1, "")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(1, "   ")

    def test_task_str_representation(self):
        """Test string representation of a task."""
        task = Task(1, "Test Title", "Test Description", False)
        assert "[○] 1. Test Title - Test Description" in str(task)

        task.completed = True
        assert "[✓] 1. Test Title - Test Description" in str(task)

    def test_task_repr_representation(self):
        """Test developer representation of a task."""
        task = Task(1, "Test Title", "Test Description", False)
        expected = "Task(id=1, title='Test Title', description='Test Description', completed=False)"
        assert expected in repr(task)

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(1, "Test Title", "Test Description", True)
        task_dict = task.to_dict()

        assert task_dict["id"] == 1
        assert task_dict["title"] == "Test Title"
        assert task_dict["description"] == "Test Description"
        assert task_dict["completed"] is True
        assert "created" in task_dict


class TestTaskList:
    """Test cases for the TaskList class."""

    def test_initialization(self):
        """Test initializing an empty TaskList."""
        task_list = TaskList()
        assert len(task_list.get_all_tasks()) == 0
        assert task_list.get_next_id() == 1

    def test_add_task(self):
        """Test adding a new task."""
        task_list = TaskList()
        task_id = task_list.add_task("Test Title", "Test Description")

        assert task_id == 1
        assert task_list.get_next_id() == 2

        tasks = task_list.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 1
        assert tasks[0].title == "Test Title"
        assert tasks[0].description == "Test Description"
        assert tasks[0].completed is False

    def test_add_task_title_validation(self):
        """Test that task title cannot be empty when adding."""
        task_list = TaskList()

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_list.add_task("")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_list.add_task("   ")

    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        task_list = TaskList()
        task_list.add_task("Task 1")
        task_list.add_task("Task 2")

        tasks = task_list.get_all_tasks()
        assert len(tasks) == 2

    def test_get_task_by_id(self):
        """Test retrieving a task by ID."""
        task_list = TaskList()
        task_id = task_list.add_task("Test Task")

        task = task_list.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "Test Task"

    def test_get_task_by_id_not_found(self):
        """Test retrieving a non-existent task."""
        task_list = TaskList()

        with pytest.raises(KeyError, match="Task with ID 1 does not exist"):
            task_list.get_task_by_id(1)

    def test_update_task(self):
        """Test updating an existing task."""
        task_list = TaskList()
        task_id = task_list.add_task("Original Title", "Original Description")

        result = task_list.update_task(task_id, "Updated Title", "Updated Description")
        assert result is True

        updated_task = task_list.get_task_by_id(task_id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"

    def test_update_task_partial(self):
        """Test updating only title or description."""
        task_list = TaskList()
        task_id = task_list.add_task("Original Title", "Original Description")

        # Update only title
        task_list.update_task(task_id, title="Updated Title")
        updated_task = task_list.get_task_by_id(task_id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original Description"

        # Update only description
        task_list.update_task(task_id, description="New Description")
        updated_task = task_list.get_task_by_id(task_id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "New Description"

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        task_list = TaskList()

        with pytest.raises(KeyError, match="Task with ID 1 does not exist"):
            task_list.update_task(1, "New Title")

    def test_update_task_title_validation(self):
        """Test that updated title cannot be empty."""
        task_list = TaskList()
        task_id = task_list.add_task("Original Title")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_list.update_task(task_id, title="")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_list.update_task(task_id, title="   ")

    def test_delete_task(self):
        """Test deleting an existing task."""
        task_list = TaskList()
        task_id = task_list.add_task("Test Task")

        result = task_list.delete_task(task_id)
        assert result is True
        assert len(task_list.get_all_tasks()) == 0

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        task_list = TaskList()

        with pytest.raises(KeyError, match="Task with ID 1 does not exist"):
            task_list.delete_task(1)

    def test_mark_task_status(self):
        """Test marking a task as complete/incomplete."""
        task_list = TaskList()
        task_id = task_list.add_task("Test Task")

        # Mark as complete
        result = task_list.mark_task_status(task_id, True)
        assert result is True

        task = task_list.get_task_by_id(task_id)
        assert task.completed is True

        # Mark as incomplete
        result = task_list.mark_task_status(task_id, False)
        assert result is True

        task = task_list.get_task_by_id(task_id)
        assert task.completed is False

    def test_mark_task_status_not_found(self):
        """Test marking status of a non-existent task."""
        task_list = TaskList()

        with pytest.raises(KeyError, match="Task with ID 1 does not exist"):
            task_list.mark_task_status(1, True)