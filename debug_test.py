from sqlmodel import SQLModel, Field
from typing import Optional

# Let's try to see if there's an issue with the 'id' name specifically
class TestModel(SQLModel, table=True):
    __tablename__ = 'test_users'  # Try adding explicit table name

    identifier: Optional[str] = Field(primary_key=True)  # Use different name
    email: str = Field(nullable=False)

print("Test model with different field name works!")