"""
Performance test for handling up to 1000 tasks
"""
import time
from src.services.todo_service import TodoService


def test_performance_with_1000_tasks():
    """Test performance with up to 1000 tasks as per NFR-1."""
    service = TodoService()

    # Add 1000 tasks
    start_time = time.time()
    for i in range(1000):
        service.add_task(f"Task {i}", f"Description for task {i}")
    add_time = time.time() - start_time

    # Verify all tasks were added
    tasks = service.get_all_tasks()
    assert len(tasks) == 1000

    # Test retrieval time
    start_time = time.time()
    tasks = service.get_all_tasks()
    retrieval_time = time.time() - start_time

    # Test individual retrieval
    start_time = time.time()
    task = service.get_task_by_id(500)
    individual_retrieval_time = time.time() - start_time

    # Test update
    start_time = time.time()
    service.update_task(500, "Updated Task 500")
    update_time = time.time() - start_time

    # Test marking status
    start_time = time.time()
    service.mark_task_status(500, True)
    mark_status_time = time.time() - start_time

    # Verify performance requirements
    # All operations should complete within 1 second as per requirements
    assert add_time < 1.0, f"Adding 1000 tasks took {add_time:.3f}s, which is too slow"
    assert retrieval_time < 1.0, f"Retrieving all tasks took {retrieval_time:.3f}s, which is too slow"
    assert individual_retrieval_time < 1.0, f"Retrieving individual task took {individual_retrieval_time:.3f}s, which is too slow"
    assert update_time < 1.0, f"Updating task took {update_time:.3f}s, which is too slow"
    assert mark_status_time < 1.0, f"Marking status took {mark_status_time:.3f}s, which is too slow"

    # Verify the updated task
    updated_task = service.get_task_by_id(500)
    assert updated_task.title == "Updated Task 500"
    assert updated_task.completed is True

    print(f"Performance test passed:")
    print(f"  - Added 1000 tasks in {add_time:.3f}s")
    print(f"  - Retrieved all tasks in {retrieval_time:.3f}s")
    print(f"  - Retrieved individual task in {individual_retrieval_time:.3f}s")
    print(f"  - Updated task in {update_time:.3f}s")
    print(f"  - Marked status in {mark_status_time:.3f}s")


if __name__ == "__main__":
    test_performance_with_1000_tasks()
    print("All performance tests passed!")