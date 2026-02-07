#!/usr/bin/env python3
"""Database connection verification script."""
import sys
import os
import inspect

# Get the current file's directory and add it to the Python path
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.services.database import db_service
from src.models.base import create_db_and_tables
from src.models.user import User
from src.models.task import Task
from sqlmodel import Session, select


def main():
    """Main verification function."""
    print("Starting backend infrastructure verification...")

    # 1. Test database connection
    print("\n1. Testing database connection...")
    try:
        is_connected = db_service.test_connection()
        if is_connected:
            print("   ✓ Database connection successful")
        else:
            print("   ✗ Database connection failed")
            sys.exit(1)
    except Exception as e:
        print(f"   ✗ Database connection error: {e}")
        sys.exit(1)

    # 2. Test table creation
    print("\n2. Testing table creation...")
    try:
        create_db_and_tables()
        print("   ✓ Tables created successfully")
    except Exception as e:
        print(f"   ✗ Table creation failed: {e}")
        sys.exit(1)

    # 3. Test basic CRUD operations
    print("\n3. Testing basic CRUD operations...")
    try:
        with db_service.get_session_context() as session:
            # Create a test user
            test_user = User(email="verification@test.com")
            session.add(test_user)
            session.commit()
            session.refresh(test_user)

            # Verify user was created
            if test_user.id and test_user.email == "verification@test.com":
                print("   ✓ User creation successful")
            else:
                print("   ✗ User creation failed")
                sys.exit(1)

            # Create a test task
            test_task = Task(title="Verification Task", user_id=test_user.id)
            session.add(test_task)
            session.commit()
            session.refresh(test_task)

            # Verify task was created
            if test_task.id and test_task.title == "Verification Task":
                print("   ✓ Task creation successful")
            else:
                print("   ✗ Task creation failed")
                sys.exit(1)

            # Test query
            statement = select(Task).where(Task.user_id == test_user.id)
            tasks = session.exec(statement).all()

            if len(tasks) >= 1:
                print("   ✓ Query operations successful")
            else:
                print("   ✗ Query operations failed")
                sys.exit(1)

            # Clean up test data
            session.delete(test_task)
            session.delete(test_user)
            session.commit()

            print("   ✓ Test data cleaned up successfully")

        print("\n4. All verification tests passed!")
        print("   ✓ Backend infrastructure is working correctly")

    except Exception as e:
        print(f"   ✗ CRUD operations failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()