"""
Unit tests for TodoService
"""
import pytest
from src.services.todo_service import TodoService


class TestTodoService:
    """Test cases for the TodoService class."""

    def test_initialization(self):
        """Test initializing TodoService."""
        service = TodoService()
        assert service.task_list is not None
        assert len(service.get_all_tasks()) == 0

    def test_add_task(self):
        """Test adding a new task."""
        service = TodoService()
        task_id = service.add_task("Test Title", "Test Description")

        assert task_id == 1
        assert service.get_next_task_id() == 2

        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 1
        assert tasks[0].title == "Test Title"
        assert tasks[0].description == "Test Description"
        assert tasks[0].completed is False

    def test_add_task_title_validation(self):
        """Test that task title cannot be empty when adding."""
        service = TodoService()

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.add_task("")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.add_task("   ")

    def test_get_all_tasks(self):
        """Test retrieving all tasks."""
        service = TodoService()
        service.add_task("Task 1")
        service.add_task("Task 2")

        tasks = service.get_all_tasks()
        assert len(tasks) == 2

    def test_get_task_by_id(self):
        """Test retrieving a task by ID."""
        service = TodoService()
        task_id = service.add_task("Test Task")

        task = service.get_task_by_id(task_id)
        assert task.id == task_id
        assert task.title == "Test Task"

    def test_get_task_by_id_not_found(self):
        """Test retrieving a non-existent task."""
        service = TodoService()

        with pytest.raises(KeyError, match="Task with ID 1 does not exist"):
            service.get_task_by_id(1)

    def test_update_task(self):
        """Test updating an existing task."""
        service = TodoService()
        task_id = service.add_task("Original Title", "Original Description")

        result = service.update_task(task_id, "Updated Title", "Updated Description")
        assert result is True

        updated_task = service.get_task_by_id(task_id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"

    def test_update_task_partial(self):
        """Test updating only title or description."""
        service = TodoService()
        task_id = service.add_task("Original Title", "Original Description")

        # Update only title
        service.update_task(task_id, title="Updated Title")
        updated_task = service.get_task_by_id(task_id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original Description"

        # Update only description
        service.update_task(task_id, description="New Description")
        updated_task = service.get_task_by_id(task_id)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "New Description"

    def test_update_task_not_found(self):
        """Test updating a non-existent task."""
        service = TodoService()

        with pytest.raises(KeyError, match="Task with ID 1 does not exist"):
            service.update_task(1, "New Title")

    def test_update_task_title_validation(self):
        """Test that updated title cannot be empty."""
        service = TodoService()
        task_id = service.add_task("Original Title")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task_id, title="")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task_id, title="   ")

    def test_delete_task(self):
        """Test deleting an existing task."""
        service = TodoService()
        task_id = service.add_task("Test Task")

        result = service.delete_task(task_id)
        assert result is True
        assert len(service.get_all_tasks()) == 0

    def test_delete_task_not_found(self):
        """Test deleting a non-existent task."""
        service = TodoService()

        with pytest.raises(KeyError, match="Task with ID 1 does not exist"):
            service.delete_task(1)

    def test_mark_task_status(self):
        """Test marking a task as complete/incomplete."""
        service = TodoService()
        task_id = service.add_task("Test Task")

        # Mark as complete
        result = service.mark_task_status(task_id, True)
        assert result is True

        task = service.get_task_by_id(task_id)
        assert task.completed is True

        # Mark as incomplete
        result = service.mark_task_status(task_id, False)
        assert result is True

        task = service.get_task_by_id(task_id)
        assert task.completed is False

    def test_mark_task_status_not_found(self):
        """Test marking status of a non-existent task."""
        service = TodoService()

        with pytest.raises(KeyError, match="Task with ID 1 does not exist"):
            service.mark_task_status(1, True)

    def test_get_next_task_id(self):
        """Test getting the next available task ID."""
        service = TodoService()
        assert service.get_next_task_id() == 1

        service.add_task("Test Task")
        assert service.get_next_task_id() == 2