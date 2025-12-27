"""
Integration tests for CLI flow and Task Management scenarios
"""
from src.services.todo_service import TodoService


class TestTaskManagementFlow:
    """Test cases for the primary Task Management Flow user scenario."""

    def test_task_management_flow(self):
        """Test the complete Task Management Flow: add, view, mark complete, exit."""
        service = TodoService()

        # Step 1: Add a new task
        task_id = service.add_task("Test Task", "This is a test task")
        assert task_id == 1

        # Step 2: View all tasks
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 1
        assert tasks[0].title == "Test Task"
        assert tasks[0].description == "This is a test task"
        assert tasks[0].completed is False

        # Step 3: Mark task as complete
        result = service.mark_task_status(1, True)
        assert result is True

        # Verify task is now complete
        task = service.get_task_by_id(1)
        assert task.completed is True

        # Test completed
        assert True


class TestTaskUpdateFlow:
    """Test cases for the Task Update Flow user scenario."""

    def test_task_update_flow(self):
        """Test the Task Update Flow: view tasks, update description, verify changes."""
        service = TodoService()

        # Add a task
        task_id = service.add_task("Original Task", "Original description")
        assert task_id == 1

        # View tasks - check initial state
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Original Task"
        assert tasks[0].description == "Original description"

        # Update the task
        result = service.update_task(1, "Updated Task", "Updated description")
        assert result is True

        # Verify the changes
        updated_task = service.get_task_by_id(1)
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated description"

        # Test completed
        assert True

    def test_task_update_validation(self):
        """Test validation during task update."""
        service = TodoService()

        # Add a task
        task_id = service.add_task("Original Task", "Original description")
        assert task_id == 1

        # Try to update with empty title - should raise ValueError
        try:
            service.update_task(1, "")
            assert False, "Expected ValueError for empty title"
        except ValueError:
            pass  # Expected

        # Task should remain unchanged
        task = service.get_task_by_id(1)
        assert task.title == "Original Task"


class TestTaskDeletionFlow:
    """Test cases for the Task Deletion Flow user scenario."""

    def test_task_deletion_flow(self):
        """Test the Task Deletion Flow: view tasks, delete task, verify removal."""
        service = TodoService()

        # Add a task
        task_id = service.add_task("Task to Delete", "Description for deletion test")
        assert task_id == 1

        # View tasks - check it exists
        tasks = service.get_all_tasks()
        assert len(tasks) == 1

        # Delete the task
        result = service.delete_task(1)
        assert result is True

        # Verify it's removed
        tasks_after = service.get_all_tasks()
        assert len(tasks_after) == 0

        # Test completed
        assert True

    def test_task_deletion_validation(self):
        """Test validation during task deletion."""
        service = TodoService()

        # Try to delete a non-existent task - should raise KeyError
        try:
            service.delete_task(999)
            assert False, "Expected KeyError for non-existent task"
        except KeyError:
            pass  # Expected


def test_full_integration():
    """Test full integration of all operations in sequence."""
    service = TodoService()

    # Add multiple tasks
    id1 = service.add_task("First Task", "Description 1")
    id2 = service.add_task("Second Task", "Description 2")
    id3 = service.add_task("Third Task")

    assert id1 == 1
    assert id2 == 2
    assert id3 == 3

    # View all tasks
    tasks = service.get_all_tasks()
    assert len(tasks) == 3

    # Update a task
    result = service.update_task(2, "Updated Second Task")
    assert result is True

    # Verify update
    updated_task = service.get_task_by_id(2)
    assert updated_task.title == "Updated Second Task"
    assert updated_task.description == "Description 2"  # Description should remain

    # Mark as complete
    result = service.mark_task_status(1, True)
    assert result is True

    # Verify completion status
    task1 = service.get_task_by_id(1)
    assert task1.completed is True

    # Delete a task
    result = service.delete_task(3)
    assert result is True

    # Verify deletion
    tasks_after = service.get_all_tasks()
    assert len(tasks_after) == 2

    # Final verification
    remaining_ids = [t.id for t in tasks_after]
    assert 1 in remaining_ids
    assert 2 in remaining_ids
    assert 3 not in remaining_ids  # Task 3 should be deleted

    # Test completed
    assert True