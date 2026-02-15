#!/usr/bin/env python3
"""Minimal test to isolate the SQLModel issue"""

from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


def generate_uuid() -> str:
    return str(uuid.uuid4())


class User(SQLModel, table=True):
    """Minimal User model for testing."""

    id: str = Field(default_factory=generate_uuid, primary_key=True)
    email: str = Field(sa_column_kwargs={"unique": True, "nullable": False})


if __name__ == "__main__":
    print("Creating user instance...")
    user = User(email="test@example.com")
    print(f"User created: {user.id}, {user.email}")
    print("Success!")