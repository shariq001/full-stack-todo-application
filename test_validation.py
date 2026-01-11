#!/usr/bin/env python3
"""
Quick validation script for the CLI Todo App.
This tests that all main functionality works together.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.models.task import Task
from src.services.manager import TaskManager
from src.ui.cli import CLI


def test_basic_functionality():
    """Test all core functionality of the Todo App."""
    print("Testing CLI Todo App functionality...\n")

    # Test Task model
    print("1. Testing Task model...")
    task = Task(id=1, title="Test Task", description="Test Description", completed=False)
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    print("   ✓ Task model works correctly")

    # Test TaskManager
    print("\n2. Testing TaskManager...")
    tm = TaskManager()

    # Add a task
    added_task = tm.add_task("Buy groceries", "Milk, bread, eggs")
    assert added_task.id == 1
    assert added_task.title == "Buy groceries"
    assert added_task.description == "Milk, bread, eggs"
    print("   ✓ Task addition works")

    # Get all tasks
    tasks = tm.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == 1
    print("   ✓ Task retrieval works")

    # Update a task
    success = tm.update_task(1, title="Buy groceries updated", description="Milk, bread, eggs, fruits")
    assert success == True
    updated_task = tm.get_task_by_id(1)
    assert updated_task.title == "Buy groceries updated"
    print("   ✓ Task update works")

    # Mark as complete
    success = tm.mark_complete(1)
    assert success == True
    completed_task = tm.get_task_by_id(1)
    assert completed_task.completed == True
    print("   ✓ Mark complete works")

    # Mark as incomplete
    success = tm.mark_incomplete(1)
    assert success == True
    incomplete_task = tm.get_task_by_id(1)
    assert incomplete_task.completed == False
    print("   ✓ Mark incomplete works")

    # Delete a task
    success = tm.remove_task(1)
    assert success == True
    assert len(tm.get_all_tasks()) == 0
    print("   ✓ Task deletion works")

    print("\n✓ All core functionality tests passed!")


def test_error_handling():
    """Test error handling capabilities."""
    print("\n3. Testing error handling...")
    tm = TaskManager()

    # Test invalid task ID
    result = tm.get_task_by_id(-1)
    assert result is None
    print("   ✓ Invalid ID handling works")

    # Test non-existent task operations
    assert tm.remove_task(999) == False
    assert tm.update_task(999, title="test") == False
    assert tm.mark_complete(999) == False
    assert tm.mark_incomplete(999) == False
    print("   ✓ Non-existent task handling works")

    # Test invalid input for task creation
    try:
        tm.add_task("")  # Empty title should raise error
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected
    print("   ✓ Invalid input validation works")

    print("   ✓ All error handling tests passed!")


if __name__ == "__main__":
    try:
        test_basic_functionality()
        test_error_handling()
        print("\n🎉 All validation tests passed! The CLI Todo App is working correctly.")
        print("\nThe application implements all 5 user stories:")
        print("- Add New Tasks")
        print("- View All Tasks")
        print("- Update Task Details")
        print("- Delete Tasks")
        print("- Mark Tasks Complete/Incomplete")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1)