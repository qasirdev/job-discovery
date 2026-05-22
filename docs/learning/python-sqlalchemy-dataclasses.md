# Learning: SQLAlchemy Dataclasses and Field Inheritance Gotchas

## Learning Objectives
- Avoid fatal application crashes during SQLAlchemy 2.0 `MappedAsDataclass` initialization.
- Understand the strict rules of standard Python `@dataclass` field ordering.

## Technical Details

### The Problem
During the integration of `MappedAsDataclass` into our base `DBJob` model in `backend/models.py`, the `uvicorn` server crashed immediately on startup with:
`TypeError: non-default argument 'source' follows default argument`

### The Cause
SQLAlchemy's `MappedAsDataclass` leverages the standard library `dataclasses` module. Python enforces a strict rule: **Fields without default values CANNOT follow fields with default values** within the same dataclass (or across an inheritance chain).

If you have:
```python
class Base(MappedAsDataclass):
    id: Mapped[int] = mapped_column(default=None) # Has default

class Child(Base):
    name: Mapped[str] # No default! This throws a TypeError.
```
Python builds the `__init__` constructor for `Child` sequentially combining the fields. It would look like `def __init__(self, id=None, name):`, which is syntactically invalid Python.

### The Solution
We fixed this in `backend/models.py` by ensuring all non-default fields (e.g. `title`, `company`, `source`) are defined *before* any fields that have defaults or leverage `default_factory=datetime.utcnow` (like `created_at`, `updated_at`). Always declare mandatory arguments at the top of your ORM models when using `MappedAsDataclass`!
