#!/usr/bin/env python3
"""Minimal test to see if SQLModel works."""

from sqlmodel import SQLModel, Field
from typing import Optional

# Very simple test
class SimpleModel(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str

print("Simple model works!")

# Now try with string ID
class SimpleModelWithStringID(SQLModel, table=True):
    id: Optional[str] = Field(primary_key=True)
    name: str

print("String ID model works!")