#!/usr/bin/env python3
"""Simple test to diagnose the model import issue."""

# Let's try importing just the basics first
try:
    from sqlmodel import SQLModel, Field, Relationship
    print("+ SQLModel imports work")
except ImportError as e:
    print(f"- Failed to import SQLModel: {e}")
    exit(1)

# Let me try a much simpler model first without the complex setup
try:
    from typing import Optional
    from datetime import datetime

    class SimpleUser(SQLModel, table=True):
        id: int = Field(primary_key=True)
        email: str

    print("+ Simple model works")

    # Now let me try the original structure from the actual codebase
    import uuid
    from sqlalchemy import Column, DateTime, String

    class User(SQLModel, table=True):
        id: str = Field(default=lambda: str(uuid.uuid4()), primary_key=True)  # Try default instead of default_factory
        email: str = Field(sa_column=Column(String, unique=True, nullable=False))
        created_at: Optional[datetime] = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), nullable=False))
        updated_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))

    print("+ User model can be defined")

    # Create an instance to make sure it works
    user = User(email="test@example.com")
    print(f"+ User instance created: {user.email}")

except Exception as e:
    print(f"- Failed to define User model: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("User model test passed!")