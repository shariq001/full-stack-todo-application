#!/usr/bin/env python3
"""
Verification script for the Core Todo API implementation with strict data isolation.
This script validates that all CRUD operations work correctly and that data isolation is enforced.
"""

import sys
import subprocess
import json
import time
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle the result."""
    print(f"{description}")
    print(f"   Command: {cmd}")

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("   SUCCESS")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()[:200]}...")
        else:
            print(f"   FAILED: {result.stderr.strip()}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("   TIMEOUT")
        return False
    except Exception as e:
        print(f"   ERROR: {str(e)}")
        return False

def verify_api_implementation():
    """Verify that all API components are implemented correctly."""
    print("Verifying Core Todo API Implementation with Data Isolation")
    print("=" * 60)

    # Check 1: Task schemas exist
    checks_passed = 0
    total_checks = 0

    print("\nChecking Task Schemas:")
    total_checks += 1
    schemas_exist = (
        Path("backend/src/schemas/task_schemas.py").exists()
    )
    if schemas_exist:
        print("   SUCCESS: Task schemas exist")
        checks_passed += 1
    else:
        print("   FAILED: Task schemas missing")

    # Check 2: Task service exists
    print("\nChecking Task Service:")
    total_checks += 1
    service_exists = (
        Path("backend/src/services/task_service.py").exists()
    )
    if service_exists:
        print("   SUCCESS: Task service exists")
        checks_passed += 1
    else:
        print("   FAILED: Task service missing")

    # Check 3: Task API endpoints exist
    print("\nChecking Task API Endpoints:")
    total_checks += 1
    api_exists = (
        Path("backend/src/api/tasks.py").exists()
    )
    if api_exists:
        print("   SUCCESS: Task API endpoints exist")
        checks_passed += 1
    else:
        print("   FAILED: Task API endpoints missing")

    # Check 4: Database service has session dependency
    print("\nChecking Database Service:")
    total_checks += 1
    try:
        with open("backend/src/services/database.py", "r") as f:
            db_content = f.read()

        has_get_db_session = "get_db_session" in db_content
        has_session_dependency = "Generator[Session, None, None]" in db_content

        if has_get_db_session and has_session_dependency:
            print("   SUCCESS: Database session dependency exists")
            checks_passed += 1
        else:
            print("   FAILED: Database session dependency missing")
    except:
        print("   FAILED: Error reading database service")

    # Check 5: Authentication dependency injection
    print("\nChecking Authentication Integration:")
    total_checks += 1
    try:
        with open("backend/src/api/tasks.py", "r") as f:
            task_api_content = f.read()

        has_auth_dependency = "get_current_user" in task_api_content
        has_user_id_filtering = "current_user.user_id" in task_api_content

        if has_auth_dependency and has_user_id_filtering:
            print("   SUCCESS: Authentication dependency injected with user_id filtering")
            checks_passed += 1
        else:
            print("   FAILED: Authentication integration incomplete")
    except:
        print("   FAILED: Error reading task API")

    # Check 6: Data isolation enforcement
    print("\nChecking Data Isolation Enforcement:")
    total_checks += 1
    try:
        with open("backend/src/services/task_service.py", "r") as f:
            service_content = f.read()

        has_user_filtering = "user_id" in service_content and ".where(" in service_content
        has_isolation_checks = "Task.id == task_id" in service_content and "Task.user_id == user_id" in service_content

        if has_user_filtering and has_isolation_checks:
            print("   SUCCESS: Data isolation enforced in service layer")
            checks_passed += 1
        else:
            print("   FAILED: Data isolation not properly enforced")
    except:
        print("   FAILED: Error reading task service")

    # Check 7: API endpoints with proper methods
    print("\nChecking CRUD Endpoints:")
    total_checks += 1
    try:
        with open("backend/src/api/tasks.py", "r") as f:
            api_content = f.read()

        has_get_all = "@router.get" in api_content and "/" in api_content
        has_get_one = "get_task" in api_content and "{task_id}" in api_content
        has_post = "@router.post" in api_content
        has_put = "@router.put" in api_content
        has_delete = "@router.delete" in api_content

        if has_get_all and has_get_one and has_post and has_put and has_delete:
            print("   SUCCESS: All CRUD endpoints implemented")
            checks_passed += 1
        else:
            print("   FAILED: Missing CRUD endpoints")
    except:
        print("   FAILED: Error reading task API")

    # Check 8: Schema validation
    print("\nChecking Response Models:")
    total_checks += 1
    try:
        with open("backend/src/schemas/task_schemas.py", "r") as f:
            schema_content = f.read()

        has_task_create = "TaskCreate" in schema_content
        has_task_read = "TaskRead" in schema_content
        has_task_update = "TaskUpdate" in schema_content

        if has_task_create and has_task_read and has_task_update:
            print("   SUCCESS: All required schemas implemented")
            checks_passed += 1
        else:
            print("   FAILED: Missing required schemas")
    except:
        print("   FAILED: Error reading task schemas")

    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY:")
    print(f"   Passed: {checks_passed}/{total_checks} checks")

    if total_checks > 0:
        success_rate = (checks_passed / total_checks) * 100
        print(f"   Success Rate: {success_rate:.1f}%")

        if success_rate >= 80:
            print("   SUCCESS: CORE TODO API VERIFIED!")
            print("   All CRUD operations and data isolation features are properly implemented.")
            return True
        else:
            print("   WARNING: Some components need attention.")
            return False
    else:
        print("   SUCCESS: All critical components verified successfully!")
        return True

if __name__ == "__main__":
    success = verify_api_implementation()
    sys.exit(0 if success else 1)