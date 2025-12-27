"""
Contract tests for the Task API as defined in the API contract
"""
import pytest
from datetime import datetime
from src.services.todo_service import TodoService
from src.models.task import Task


class TestTaskApiContract:
    """Contract tests for the Task API methods."""

    def test_add_task_contract(self):
        """Test add_task method per contract: add_task(title: str, description: str = "") -> int"""
        service = TodoService()

        # Test with title only
        task_id = service.add_task("Test Title")
        assert isinstance(task_id, int)
        assert task_id > 0

        # Test with title and description
        task_id2 = service.add_task("Test Title 2", "Test Description")
        assert isinstance(task_id2, int)
        assert task_id2 > task_id

        # Test error case: empty title
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.add_task("")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.add_task("   ")

    def test_get_all_tasks_contract(self):
        """Test get_all_tasks method per contract: get_all_tasks() -> List[Task]"""
        service = TodoService()

        # Test with empty list
        tasks = service.get_all_tasks()
        assert isinstance(tasks, list)
        assert len(tasks) == 0

        # Test with items
        service.add_task("Task 1")
        service.add_task("Task 2")

        tasks = service.get_all_tasks()
        assert isinstance(tasks, list)
        assert len(tasks) == 2
        assert all(isinstance(task, Task) for task in tasks)

    def test_get_task_by_id_contract(self):
        """Test get_task_by_id method per contract: get_task_by_id(task_id: int) -> Task"""
        service = TodoService()

        # Add a task
        task_id = service.add_task("Test Task", "Test Description")

        # Test retrieval
        task = service.get_task_by_id(task_id)
        assert isinstance(task, Task)
        assert task.id == task_id
        assert task.title == "Test Task"
        assert task.description == "Test Description"

        # Test error case: non-existent ID
        with pytest.raises(KeyError, match="Task with ID 999 does not exist"):
            service.get_task_by_id(999)

    def test_update_task_contract(self):
        """Test update_task method per contract: update_task(task_id: int, title: str = None, description: str = None) -> bool"""
        service = TodoService()

        # Add a task
        task_id = service.add_task("Original Title", "Original Description")

        # Test update with new title
        result = service.update_task(task_id, "New Title")
        assert result is True

        task = service.get_task_by_id(task_id)
        assert task.title == "New Title"
        assert task.description == "Original Description"

        # Test update with new description
        result = service.update_task(task_id, description="New Description")
        assert result is True

        task = service.get_task_by_id(task_id)
        assert task.title == "New Title"
        assert task.description == "New Description"

        # Test update with both
        result = service.update_task(task_id, "Final Title", "Final Description")
        assert result is True

        task = service.get_task_by_id(task_id)
        assert task.title == "Final Title"
        assert task.description == "Final Description"

        # Test error case: non-existent ID
        with pytest.raises(KeyError, match="Task with ID 999 does not exist"):
            service.update_task(999, "New Title")

        # Test error case: empty title
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(task_id, "")

    def test_delete_task_contract(self):
        """Test delete_task method per contract: delete_task(task_id: int) -> bool"""
        service = TodoService()

        # Add a task
        task_id = service.add_task("Test Task")

        # Test deletion
        result = service.delete_task(task_id)
        assert result is True

        # Verify task is gone
        with pytest.raises(KeyError, match=f"Task with ID {task_id} does not exist"):
            service.get_task_by_id(task_id)

        # Test error case: non-existent ID
        with pytest.raises(KeyError, match="Task with ID 999 does not exist"):
            service.delete_task(999)

    def test_mark_task_status_contract(self):
        """Test mark_task_status method per contract: mark_task_status(task_id: int, completed: bool) -> bool"""
        service = TodoService()

        # Add a task
        task_id = service.add_task("Test Task")

        # Test marking as complete
        result = service.mark_task_status(task_id, True)
        assert result is True

        task = service.get_task_by_id(task_id)
        assert task.completed is True

        # Test marking as incomplete
        result = service.mark_task_status(task_id, False)
        assert result is True

        task = service.get_task_by_id(task_id)
        assert task.completed is False

        # Test error case: non-existent ID
        with pytest.raises(KeyError, match="Task with ID 999 does not exist"):
            service.mark_task_status(999, True)


def test_task_model_contract():
    """Test Task model properties as defined in the contract."""
    # Create a task
    task = Task(1, "Test Title", "Test Description", False)

    # Test properties
    assert task.id == 1
    assert task.title == "Test Title"
    assert task.description == "Test Description"
    assert task.completed is False
    assert isinstance(task.created, datetime)

    # Test string representation
    task_str = str(task)
    assert "[○]" in task_str  # Incomplete marker
    assert "1." in task_str
    assert "Test Title" in task_str

    # Test completion status change in string representation
    task.completed = True
    task_str_completed = str(task)
    assert "[✓]" in task_str_completed  # Complete marker

    # Test to_dict method
    task_dict = task.to_dict()
    assert task_dict["id"] == 1
    assert task_dict["title"] == "Test Title"
    assert task_dict["description"] == "Test Description"
    assert task_dict["completed"] is True  # Changed to True above
    assert "created" in task_dict

    # Test error case: empty title
    with pytest.raises(ValueError, match="Task title cannot be empty"):
        Task(1, "")

    with pytest.raises(ValueError, match="Task title cannot be empty"):
        Task(1, "   ")