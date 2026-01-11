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
    print("   [PASS] Task model works correctly")

    # Test TaskManager
    print("\n2. Testing TaskManager...")
    tm = TaskManager()

    # Add a task
    added_task = tm.add_task("Buy groceries", "Milk, bread, eggs")
    assert added_task.id == 1
    assert added_task.title == "Buy groceries"
    assert added_task.description == "Milk, bread, eggs"
    print("   [PASS] Task addition works")

    # Get all tasks
    tasks = tm.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].id == 1
    print("   [PASS] Task retrieval works")

    # Update a task
    success = tm.update_task(1, title="Buy groceries updated", description="Milk, bread, eggs, fruits")
    assert success == True
    updated_task = tm.get_task_by_id(1)
    assert updated_task.title == "Buy groceries updated"
    print("   [PASS] Task update works")

    # Mark as complete
    success = tm.mark_complete(1)
    assert success == True
    completed_task = tm.get_task_by_id(1)
    assert completed_task.completed == True
    print("   [PASS] Mark complete works")

    # Mark as incomplete
    success = tm.mark_incomplete(1)
    assert success == True
    incomplete_task = tm.get_task_by_id(1)
    assert incomplete_task.completed == False
    print("   [PASS] Mark incomplete works")

    # Delete a task
    success = tm.remove_task(1)
    assert success == True
    assert len(tm.get_all_tasks()) == 0
    print("   [PASS] Task deletion works")

    print("\n[PASS] All core functionality tests passed!")


def test_error_handling():
    """Test error handling capabilities."""
    print("\n3. Testing error handling...")
    tm = TaskManager()

    # Test invalid task ID
    result = tm.get_task_by_id(-1)
    assert result is None
    print("   [PASS] Invalid ID handling works")

    # Test non-existent task operations
    assert tm.remove_task(999) == False
    assert tm.update_task(999, title="test") == False
    assert tm.mark_complete(999) == False
    assert tm.mark_incomplete(999) == False
    print("   [PASS] Non-existent task handling works")

    # Test invalid input for task creation
    try:
        tm.add_task("")  # Empty title should raise error
        assert False, "Should have raised ValueError"
    except ValueError:
        pass  # Expected
    print("   [PASS] Invalid input validation works")

    print("   [PASS] All error handling tests passed!")


if __name__ == "__main__":
    try:
        test_basic_functionality()
        test_error_handling()
        print("\n[PASS] All validation tests passed! The CLI Todo App is working correctly.")
        print("\nThe application implements all 5 user stories:")
        print("- Add New Tasks")
        print("- View All Tasks")
        print("- Update Task Details")
        print("- Delete Tasks")
        print("- Mark Tasks Complete/Incomplete")

        # Mark the final task as completed
        import fileinput
        import re

        # Update the tasks file to mark the final task as complete
        with fileinput.FileInput("specs/001-cli-todo-app/tasks.md", inplace=True) as file:
            for line in file:
                if line.strip() == "- [ ] T045 Run quickstart validation to ensure all features work together":
                    print("- [X] T045 Run quickstart validation to ensure all features work together")
                else:
                    print(line, end='')

    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        sys.exit(1)