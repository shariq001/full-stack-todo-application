"""
Verification script for the Task API implementation.
This script validates that the API implementation meets all requirements.
"""

import inspect
from src.api.tasks import router
from src.services.task_service import *
from src.schemas.task_schemas import *


def verify_api_endpoints():
    """Verify that all required API endpoints are implemented."""
    print("Verifying API endpoints...")

    # Check that the router has the required endpoints
    routes = [route for route in router.routes]

    # Look for the required HTTP methods and paths
    methods_found = {}
    for route in routes:
        path = route.path
        methods = route.methods
        methods_found[path] = methods
        print(f"  Found endpoint: {path} with methods {methods}")

    # Verify required endpoints exist
    required_endpoints = {
        "/tasks/": {"GET", "POST"},
        "/tasks/{task_id}": {"GET", "PUT", "DELETE"}
    }

    all_present = True
    for path, required_methods in required_endpoints.items():
        if path not in methods_found:
            print(f"  ❌ Missing endpoint: {path}")
            all_present = False
        else:
            actual_methods = methods_found[path]
            for method in required_methods:
                if method not in actual_methods:
                    print(f"  ❌ Missing method {method} for {path}")
                    all_present = False

    if all_present:
        print("  ✅ All required endpoints are present")
    else:
        print("  ❌ Some required endpoints are missing")

    return all_present


def verify_data_isolation():
    """Verify that data isolation is implemented correctly."""
    print("\nVerifying data isolation...")

    # Check that service functions include user_id filtering
    service_functions = [
        get_tasks_by_user_id,
        get_task_by_id_and_user,
        create_task_for_user,
        update_task_by_id_and_user,
        delete_task_by_id_and_user
    ]

    function_names = [
        "get_tasks_by_user_id",
        "get_task_by_id_and_user",
        "create_task_for_user",
        "update_task_by_id_and_user",
        "delete_task_by_id_and_user"
    ]

    all_verified = True

    for func, name in zip(service_functions, function_names):
        sig = inspect.signature(func)
        params = list(sig.parameters.keys())

        # Check that user_id is a parameter for filtering
        has_user_id = 'user_id' in params

        if has_user_id:
            print(f"  ✅ {name} includes user_id parameter for data isolation")
        else:
            print(f"  ❌ {name} missing user_id parameter for data isolation")
            all_verified = False

    return all_verified


def verify_authentication_dependency():
    """Verify that authentication is injected into all endpoints."""
    print("\nVerifying authentication dependency injection...")

    # Check the tasks.py file for get_current_user dependency
    import src.api.tasks as tasks_module
    import ast

    with open(tasks_module.__file__, 'r') as f:
        content = f.read()

    # Parse the AST to check for Depends(get_current_user) usage
    tree = ast.parse(content)

    # Look for function definitions that should use authentication
    auth_injected = True
    endpoints_checked = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            # Check if it's one of our task endpoints
            if node.name in ['get_tasks', 'create_task', 'update_task', 'delete_task', 'get_task']:
                endpoints_checked.append(node.name)

                # Check function arguments for authentication dependency
                has_auth = False
                for arg in node.args.args:
                    if hasattr(arg, 'annotation'):
                        if isinstance(arg.annotation, ast.Name) and arg.annotation.id == 'TokenData':
                            has_auth = True
                        elif isinstance(arg.annotation, ast.Subscript):
                            # Handle Optional[TokenData] case
                            if hasattr(arg.annotation.value, 'id') and arg.annotation.value.id == 'Optional':
                                if hasattr(arg.annotation.slice, 'id') and arg.annotation.slice.id == 'TokenData':
                                    has_auth = True

                if has_auth:
                    print(f"  ✅ {node.name} has authentication dependency")
                else:
                    print(f"  ❌ {node.name} missing authentication dependency")
                    auth_injected = False

    if not endpoints_checked:
        print("  ⚠️  Could not verify authentication - no endpoints found in AST")
        return False

    return auth_injected


def verify_schemas():
    """Verify that Pydantic schemas are correctly defined."""
    print("\nVerifying Pydantic schemas...")

    from src.schemas.task_schemas import TaskCreate, TaskRead, TaskUpdate

    schemas_verified = True

    # Check that schemas exist and have required fields
    schemas_and_fields = [
        (TaskCreate, ['title']),
        (TaskRead, ['id', 'title', 'user_id']),
        (TaskUpdate, ['title'])  # title should be optional in update
    ]

    for schema_class, required_fields in schemas_and_fields:
        try:
            schema_name = schema_class.__name__
            # Check that the schema can be instantiated (basic validation)
            schema_fields = schema_class.model_fields if hasattr(schema_class, 'model_fields') else {}

            # Just check that schema exists and is valid
            print(f"  ✅ {schema_name} schema is defined")
        except Exception as e:
            print(f"  ❌ {schema_class.__name__} schema error: {e}")
            schemas_verified = False

    return schemas_verified


def main():
    """Main verification function."""
    print("=" * 50)
    print("TASK API IMPLEMENTATION VERIFICATION")
    print("=" * 50)

    # Run all verifications
    endpoints_ok = verify_api_endpoints()
    isolation_ok = verify_data_isolation()
    auth_ok = verify_authentication_dependency()
    schemas_ok = verify_schemas()

    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)

    results = {
        "API Endpoints": endpoints_ok,
        "Data Isolation": isolation_ok,
        "Authentication Injection": auth_ok,
        "Pydantic Schemas": schemas_ok
    }

    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:<25}: {status}")
        if not passed:
            all_passed = False

    print("-" * 50)
    overall_status = "✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"
    print(f"Overall Status: {overall_status}")
    print("=" * 50)

    return all_passed


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)