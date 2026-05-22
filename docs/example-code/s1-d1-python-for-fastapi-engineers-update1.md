```
<prompt>
 @jobs-list/2026-python-ai-azure-roadmap-v2.md
go and create file according to @jobs-list/2026-learning-prompt-v3.md in folder learning-sprints for:
- **Mon 20 Apr** — Python for TypeScript Engineers: typing, dataclasses, Pydantic v2 models, `async/await` patterns. Direct mental-model mapping from TS. Set up `pyenv`, `poetry` package manager, `ruff` linter, `mypy`, and VS Code Python profile. Write your first typed module.
</prompt>
```

# Sprint 1 · Day 1 · Mon 20 Apr 2026

**Topic:** Python for TypeScript Engineers: typing, dataclasses, Pydantic v2 models, `async/await` patterns. Direct mental-model mapping from TS.
Set up `uv` (modern) or `poetry` (legacy) package manager, `ruff` linter, `mypy`, and VS Code Python profile. Write your first typed module.

---

## Step 1: Progressive Learning Steps & UK Job Market Relevance

### 🎯 Learning Objectives

This day covers the foundational Python patterns that TypeScript engineers need to become productive in Python backend development, specifically targeting:

1. **Type Systems & Static Analysis**
   - Python's gradual typing system (typing module, type hints)
   - `mypy` for static type checking (equivalent to TypeScript compiler)
   - Runtime validation with Pydantic v2 (like Zod but integrated into models)
   - PEP 695 `type` statement — the 2026 standard for type aliases and generics

2. **Modern Python Tooling**
   - `uv` for Python version management, virtual environments, and dependency management (like nvm + npm/pnpm, but Rust-based and significantly faster) — the 2026 default
   - `poetry` for dependency management in existing codebases (like npm/pnpm with better lockfiles) — still common in interviews
   - `ruff` for linting and formatting (like ESLint + Prettier, but 100× faster)
   - `fastapi dev` as the 2026 standard development server command (hot reload); `fastapi run` for production
   - VS Code Python profile configuration

3. **Data Structures & Validation**
   - `dataclasses` for typed data structures (similar to TypeScript interfaces + classes)
   - Pydantic v2 models for runtime validation and serialisation
   - Mental model mapping: TS types → Python types
   - `Annotated` — the foundation for FastAPI dependency injection (Days 2+)

4. **Async/Await Patterns**
   - Python's `asyncio` event loop vs Node.js event loop
   - `async def` and `await` syntax (nearly identical to TS)
   - Common patterns: concurrent requests, async context managers

### 📊 UK Job Market Relevance (£90k–£130k / £550–£750/day)

| Skill Area               | Market Frequency      | Interview Focus | Why It Matters                                                                                                    |
| ------------------------ | --------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Python typing & mypy** | ~85% of senior roles  | High            | Type safety is expected in production codebases; interviewers test understanding of `Optional`, `Union`, generics |
| **Pydantic v2**          | ~60% of FastAPI roles | Very High       | De facto standard for API validation; most FastAPI projects use it extensively                                    |
| **uv**                   | ~55% of new projects  | Medium-High     | Modern default tooling; Rust-based speed; manages Python versions, venvs, and deps in one tool                    |
| **poetry**               | ~40% of roles         | Medium          | Still prevalent in existing codebases; frequently seen in interviews — senior engineers know both                 |
| **async/await**          | ~70% of backend roles | High            | FastAPI is async-first; understanding event loops and concurrency is critical                                     |
| **dataclasses**          | ~50% of roles         | Medium          | Clean data modelling; often compared to TypeScript interfaces in interviews                                       |

### ✅ Key Industry Patterns for 2026

- **Type hints are mandatory** in production Python codebases at senior level
- **Pydantic v2** (released 2023) is 5–50× faster than v1 and uses a Rust core
- **PEP 695 `type` statement** (Python 3.12+, standard in 3.14) is the 2026 standard for type aliases — replaces `TypeAlias` and bare assignment
- **`ruff`** (Rust-based linter) has become the standard, replacing pylint/flake8/black
- **`uv`** is the 2026 default for Python version management, virtual environments, and dependency installation — Rust-based, all-in-one
- **`poetry`** remains common in existing codebases and is frequently asked about in interviews — senior engineers know both
- **`fastapi dev`** (via `fastapi[standard]`) is the 2026 standard dev server (hot reload) — `fastapi run` is used in production
- UK employers expect familiarity with VS Code Python extensions and debugging

### 💼 What UK Interviewers Will Ask

- "How do you handle type safety in Python?" → typing module, mypy, Pydantic
- "Explain the difference between dataclasses and Pydantic models" → runtime validation, serialisation
- "How does Python's async/await differ from JavaScript?" → single-threaded event loop, Global Interpreter Lock (GIL) implications
- "What's your Python tooling setup?" → uv (or poetry), ruff, mypy, pytest
- "What is `uv` and why would you use it?" → Rust-based all-in-one tool: Python version management, venvs, and dependency resolution
- "When would you still use poetry over uv?" → existing codebases, team familiarity, mature plugin ecosystem
- "Should senior engineers know both uv and poetry?" → YES
- "What is `Annotated` used for?" → type metadata, FastAPI `Depends()`, PEP 593

---

## Step 2: Comprehensive Q&A and Code Artefacts

---

## 📦 Required Packages

First, set up your Python environment:

```bash
# --- Using uv (recommended) ---
# Install uv (Rust-based all-in-one tool: Python + venv + deps)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python 3.14
uv python install 3.14
uv python pin 3.14  # creates .python-version file

# Create new project
uv init python-for-ts-engineers
cd python-for-ts-engineers

# Add core dependencies
uv add pydantic pydantic-settings

# Add dev dependencies
uv add --dev ruff mypy pytest pytest-asyncio pytest-cov httpx

# Run commands (no activation needed)
uv run pytest
uv run mypy .
uv run ruff check .
```

```bash
# --- Using poetry (common in existing codebases) ---
# Install Python 3.14 (poetry uses system Python; pair with pyenv if needed)
# pyenv is legacy — prefer uv python install above
curl -sSL https://install.python-poetry.org | python3 -

# Create new project
poetry new python-for-ts-engineers
cd python-for-ts-engineers

# Add dev dependencies
poetry add --group dev ruff mypy pytest pytest-asyncio

# Add core dependencies
poetry add pydantic pydantic-settings
```

```toml
# pyproject.toml — current version pins (May 2026)
# uv-managed project
[project]
name = "python-for-ts-engineers"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = [
    "pydantic>=2.11",
    "pydantic-settings>=2.7",
]

[tool.uv]
dev-dependencies = [
    "ruff>=1.0",
    "mypy>=1.18",
    "pytest>=8",
    "pytest-asyncio>=0.24",
    "pytest-cov>=6",
    "httpx>=0.28",
]

# --- poetry equivalent (legacy/existing codebases) ---
# [tool.poetry.dependencies]
# python = "^3.14"
# pydantic = "^2.11"
# pydantic-settings = "^2.7"
#
# [tool.poetry.group.dev.dependencies]
# ruff = "^1.0"
# mypy = "^1.18"
# pytest = "^8"
# pytest-asyncio = "^0.24"
# pytest-cov = "^6"
# httpx = "^0.28"

[tool.ruff]
line-length = 100
target-version = "py314"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.14"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --cov=. --cov-report=term-missing"
```

| Package             | Version (stable May 2026) | Purpose                                                                 |
| ------------------- | ------------------------- | ----------------------------------------------------------------------- |
| `pydantic`          | 2.11.x                    | Runtime validation and serialisation                                    |
| `pydantic-settings` | 2.7.x                     | Env-var config management                                               |
| `ruff`              | 1.x                       | Linter + formatter (replaces pylint, flake8, black, isort)              |
| `mypy`              | 1.18.x                    | Static type checker                                                     |
| `pytest`            | 8.x                       | Test framework                                                          |
| `pytest-asyncio`    | 0.24.x                    | Async test runner — `asyncio_mode = "auto"` removes per-test decorators |

---

## 🖥️ Part 1: Type Systems & Mental Model Mapping

### Q&A Batch 1: Python Type Hints vs TypeScript

**Q1: How do Python type hints compare to TypeScript types?**
A: Both are optional and checked statically (mypy/tsc), but Python hints are erased at runtime. Use `typing` module for generics, unions, and optionals. TypeScript is stricter by default.

```python
# Python with type hints
def greet(name: str) -> str:
    """greet function docstring."""
    return f"Hello, {name}"

# TypeScript equivalent
# function greet(name: string): string {
#     return `Hello, ${name}`;
# }
```

**Q2: What is the Python equivalent of TypeScript's `string | number`?**
A: `Union[str, int]` or modern syntax `str | int` (Python 3.10+). Use `from typing import Union` for older versions.

```python
from typing import Union

def process(value: str | int) -> str:  # Python 3.10+ — preferred
    """process function docstring."""
    return str(value)

# Legacy syntax — avoid in new code
def process_old(value: Union[str, int]) -> str:
    """process_old function docstring."""
    return str(value)
```

**Q3: How do you handle nullable types in Python?**
A: `Optional[T]` is shorthand for `Union[T, None]`. Modern syntax: `T | None` (Python 3.10+). Use `T | None` in all new code.

```python
from typing import Optional

def find_user(id: int) -> str | None:   # preferred — modern syntax
    """find_user function docstring."""
    return "John" if id == 1 else None

# Legacy — still valid but verbose
def find_user_legacy(id: int) -> Optional[str]:
    """find_user_legacy function docstring."""
    return "John" if id == 1 else None
```

**Q4: What's the Python equivalent of TypeScript interfaces?**
A: `Protocol` from `typing` for structural typing, or `dataclass`/Pydantic models for nominal typing.

```python
from typing import Protocol

class Drawable(Protocol):
    """Drawable class docstring."""
    def draw(self) -> None: ...
        """draw method docstring."""

class Circle:
    """Circle class docstring."""
    def draw(self) -> None:
        """draw method docstring."""
        print("Drawing circle")

def render(shape: Drawable) -> None:  # Duck typing — Circle satisfies Drawable
    """render function docstring."""
    shape.draw()
```

**Q5: How do generics work in Python — old style vs PEP 695?**
A: Before Python 3.14: `TypeVar` + `Generic`. Python 3.14+ (PEP 695): native `type` syntax with bracket notation — the 2026 standard, available in Python 3.14.

```python
from typing import TypeVar, Generic

# Pre-3.14 style — still works, but legacy in new projects
T = TypeVar("T")

def first_legacy(items: list[T]) -> T | None:
    """first_legacy function docstring."""
    return items[0] if items else None

class Box_legacy(Generic[T]):
    """Box_legacy class docstring."""
    def __init__(self, value: T):
        """__init__ method docstring."""
        self.value = value

# PEP 695 style — Python 3.14+ — the 2026 standard
def first[T](items: list[T]) -> T | None:
    """first function docstring."""
    return items[0] if items else None

class Box[T]:
    """Box class docstring."""
    def __init__(self, value: T) -> None:
        """__init__ method docstring."""
        self.value = value

    def get(self) -> T:
        """get method docstring."""
        return self.value
```

**Q6: What's Python's equivalent of `any` and `unknown`?**
A: `Any` allows anything (no checking). Python has no direct `unknown` equivalent; use `object` for maximum safety.

```python
from typing import Any

def process_any(value: Any) -> None:  # No type checking — avoid in production
    """process_any function docstring."""
    value.anything_goes()  # mypy won't complain

def process_object(value: object) -> None:  # Safer — mypy enforces type narrowing
    """process_object function docstring."""
    # value.method()  # mypy error: object has no method
    if isinstance(value, str):
        print(value.upper())  # safe after narrowing
```

**Q7: How do you type a dictionary in Python?**
A: `dict[KeyType, ValueType]` (modern, Python 3.9+) or `Dict[KeyType, ValueType]` (legacy — avoid).

```python
# Modern — preferred
user_ages: dict[str, int] = {"Alice": 30, "Bob": 25}

# Legacy — avoid in new code
from typing import Dict
legacy_ages: Dict[str, int] = {"Charlie": 35}
```

**Q8: What's the Python equivalent of TypeScript's `Record<K, V>`?**
A: `dict[K, V]` is close, but for stricter typing use `TypedDict`.

```python
from typing import TypedDict

class UserRecord(TypedDict):
    """UserRecord class docstring."""
    name: str
    age: int
    email: str

user: UserRecord = {"name": "Alice", "age": 30, "email": "a@b.com"}
```

**Q9: How do you type functions in Python?**
A: Use `Callable[[ArgTypes], ReturnType]` from `typing`.

```python
from typing import Callable

def apply(fn: Callable[[int, int], int], a: int, b: int) -> int:
    """apply function docstring."""
    return fn(a, b)

def add(x: int, y: int) -> int:
    """add function docstring."""
    return x + y

result = apply(add, 5, 3)  # 8
```

**Q10: What's Python's equivalent of literal types?**
A: `Literal` from `typing` (Python 3.8+).

```python
from typing import Literal

def set_mode(mode: Literal["read", "write", "append"]) -> None:
    """set_mode function docstring."""
    print(f"Mode: {mode}")

set_mode("read")   # OK
# set_mode("delete")  # mypy error
```

**Q11: How do you use `mypy` to check types?**
A: Run `mypy your_file.py` or `mypy .` for the entire project. Configure in `pyproject.toml`.

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.14"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**Q12: What's the difference between `list` and `List` in type hints?**
A: Lowercase `list[T]` is modern (Python 3.9+) — always use this. Uppercase `List[T]` requires `from typing import List` and is legacy.

```python
# Modern (preferred in all new code)
names: list[str] = ["Alice", "Bob"]

# Legacy — avoid
from typing import List
legacy_names: List[str] = ["Charlie"]
```

**Q13: How do you type variadic functions in Python?**
A: Use `*args: T` and `**kwargs: T` with type hints.

```python
def concat(*strings: str) -> str:
    """concat function docstring."""
    return "".join(strings)

def configure(**options: bool) -> dict[str, bool]:
    """configure function docstring."""
    return options

result = concat("Hello", " ", "World")
config = configure(debug=True, verbose=False)
```

**Q14: What's Python's equivalent of TypeScript's `Partial<T>`?**
A: No built-in equivalent. Use `TypedDict(total=False)` or Pydantic models with all-optional fields.

```python
from typing import TypedDict

class User(TypedDict, total=False):  # All fields optional
    """User class docstring."""
    name: str
    age: int

partial_user: User = {"name": "Alice"}  # age omitted — OK
```

**Q15: What is `Annotated` and why is it foundational for FastAPI?**
A: `Annotated[Type, metadata]` (PEP 593, Python 3.9+) attaches metadata to a type hint without changing the type itself. FastAPI reads `Depends()`, `Query()`, `Path()`, and `Header()` from the metadata slot. It is the core of the 2026 idiomatic dependency injection style (introduced fully on Day 2).

```python
from typing import Annotated

# Standalone — type is still int; the string is metadata
UserId = Annotated[int, "database primary key"]

# FastAPI usage (Day 2 onwards) — Depends() lives in the metadata slot
# type CurrentUser = Annotated[User, Depends(get_current_user)]
# async def route(user: CurrentUser) -> UserResponse: ...
```

---

### 🎯 Working Code Artefact 1: Type System Comparison

```python
"""
Type System Comparison: TypeScript mental models mapped to Python
Demonstrates common patterns TS engineers need in Python
Requires Python 3.14+ for PEP 695 generic syntax
"""

from typing import (
    TypeVar, Generic, Protocol, Callable,
    Literal, TypedDict, Annotated
)

# 1. Basic types
def greet(name: str, age: int) -> str:
    """greet function docstring."""
    return f"{name} is {age} years old"

# 2. Union types (TS: string | number)
def process_id(value: str | int) -> str:
    """process_id function docstring."""
    return str(value).upper()

# 3. Optional types (TS: string | null | undefined)
def find_user(id: int) -> str | None:
    """find_user function docstring."""
    users = {1: "Alice", 2: "Bob"}
    return users.get(id)

# 4. Literal types (TS: 'read' | 'write')
def open_file(mode: Literal["read", "write", "append"]) -> None:
    """open_file function docstring."""
    print(f"Opening file in {mode} mode")

# 5. PEP 695 generic function (Python 3.14 — the 2026 standard)
def first[T](items: list[T]) -> T | None:
    """first function docstring."""
    return items[0] if items else None

# 6. PEP 695 generic class (TS: class Box<T>)
class Box[T]:
    """Box class docstring."""
    def __init__(self, value: T) -> None:
        """__init__ method docstring."""
        self.value = value

    def get(self) -> T:
        """get method docstring."""
        return self.value

# 7. Pre-3.14 generics — still valid; understand both for reading existing codebases
_T = TypeVar("_T")

def first_legacy(items: list[_T]) -> _T | None:
    """first_legacy function docstring."""
    return items[0] if items else None

class BoxLegacy(Generic[_T]):
    """BoxLegacy class docstring."""
    def __init__(self, value: _T) -> None:
        """__init__ method docstring."""
        self.value = value

# 8. Protocols (TS: interface with structural typing)
class Serializable(Protocol):
    """Serializable class docstring."""
    def to_json(self) -> dict: ...
        """to_json method docstring."""

class User:
    """User class docstring."""
    def __init__(self, name: str) -> None:
        """__init__ method docstring."""
        self.name = name

    def to_json(self) -> dict:
        """to_json method docstring."""
        return {"name": self.name}

def save(obj: Serializable) -> None:
    """save function docstring."""
    print(f"Saving: {obj.to_json()}")

# 9. TypedDict (TS: type/interface for objects)
class UserDict(TypedDict):
    """UserDict class docstring."""
    name: str
    age: int
    email: str

def create_user(data: UserDict) -> UserDict:
    """create_user function docstring."""
    return data

# 10. Callable (TS: (x: number) => number)
def apply_twice(fn: Callable[[int], int], value: int) -> int:
    """apply_twice function docstring."""
    return fn(fn(value))

# 11. Annotated — metadata slot used by FastAPI on Day 2
type UserId = Annotated[int, "database primary key"]  # PEP 695 + PEP 593 combined

# 12. Complex nested types
ApiResponse = dict[str, list[dict[str, int | str]]]

def parse_response(data: ApiResponse) -> list[str]:
    """parse_response function docstring."""
    return [item["name"] for items in data.values()
            for item in items if "name" in item]


if __name__ == "__main__":
    """Only run this block of code if I am executing this file directly. 
    Do not run it if I am just importing this file into another script"""

    print(greet("Alice", 30))
    print(process_id(123))
    print(find_user(1))   # Alice
    print(find_user(99))  # None
    open_file("read")

    # PEP 695 generics
    print(first([1, 2, 3]))      # 1
    print(first(["a", "b"]))     # a

    int_box: Box[int] = Box(42)
    str_box: Box[str] = Box("hello")
    print(int_box.get())
    print(str_box.get())

    user = User("Bob")
    save(user)

    user_data: UserDict = {"name": "Charlie", "age": 25, "email": "c@example.com"}
    print(create_user(user_data))

    result = apply_twice(lambda x: x * 2, 5)  # (5*2)*2 = 20
    print(result)
```

### ✅ Key Concepts

- **Type hints are optional but enforced by mypy**: Unlike TypeScript, Python runs without checking types unless you explicitly run `mypy`
- **PEP 695 native generics (`def fn[T]`, `class Box[T]`)**: The 2026 standard — no `TypeVar` import needed for new code
- **Structural typing with Protocol**: Duck typing with type safety, similar to TypeScript interfaces
- **`Annotated` is the metadata foundation**: Used by FastAPI, pydantic, and the typing ecosystem — understand it on Day 1
- **Runtime vs compile-time**: Python types are erased at runtime; use Pydantic for runtime validation

### ⚠️ Common Pitfalls

- Forgetting to run `mypy` — types are not checked at runtime
- Using `Any` too liberally — defeats the purpose of type hints
- Mixing legacy (`List`, `Dict`) and modern (`list`, `dict`) syntax in the same file
- Using the pre-3.14 `TypeVar` style in new code when PEP 695 syntax is available
- Not configuring `mypy` strict mode in production projects

---

## 🖥️ Part 2: Dataclasses (TS: Classes + Interfaces)

### Q&A Batch 2: Dataclasses

**Q16: What are dataclasses and why use them?**
A: Auto-generate `__init__`, `__repr__`, `__eq__` methods. Similar to TS classes with constructor property shorthand. Use for simple data containers.

```python
from dataclasses import dataclass

@dataclass
class User:
    """User class docstring."""
    name: str
    age: int
    email: str

user = User("Alice", 30, "a@b.com")
print(user)  # User(name='Alice', age=30, email='a@b.com')
```

**Q17: How do you set default values in dataclasses?**
A: Use normal assignment. For mutable defaults (lists, dicts), use `field(default_factory=...)`.

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    """Config class docstring."""
    debug: bool = False
    tags: list[str] = field(default_factory=list)      # mutable default → []
    settings: dict[str, str] = field(default_factory=dict)  # → {}
    default_roles: list[str] = field(default_factory=lambda: ["user", "guest"])

config = Config()
print(config.debug)  # False
print(config.tags)   # []
```

**Q18: What's the difference between dataclasses and regular classes?**
A: Dataclasses auto-generate boilerplate. Regular classes require manual `__init__`, `__repr__`, etc. Use dataclasses for data containers; regular classes for behaviour-heavy objects.

```python
# Regular class (verbose)
class UserRegular:
    """UserRegular class docstring."""
    def __init__(self, name: str, age: int) -> None:
        """__init__ method docstring."""
        self.name = name
        self.age = age

    def __repr__(self) -> str:
        """__repr__ method docstring."""
        return f"User(name={self.name}, age={self.age})"

# Dataclass (concise — generates the same code above automatically)
@dataclass
class UserDataclass:
    """UserDataclass class docstring."""
    name: str
    age: int
```

**Q19: Can dataclasses be frozen (immutable)?**
A: Yes, use `@dataclass(frozen=True)`. Similar to TypeScript's `readonly` properties.

```python
@dataclass(frozen=True)
class Point:
    """Point class docstring."""
    x: int
    y: int

p = Point(1, 2)
# p.x = 3  # Raises FrozenInstanceError
```

**Q20: How do you convert dataclasses to dictionaries?**
A: Use `asdict()` from the `dataclasses` module.

```python
from dataclasses import dataclass, asdict

@dataclass
class User:
    """User class docstring."""
    name: str
    age: int

user = User("Alice", 30)
print(asdict(user))  # {'name': 'Alice', 'age': 30}
```

**Q21: Can dataclasses have methods?**
A: Yes, they are normal classes with auto-generated boilerplate methods. Add any methods as usual.

```python
@dataclass
class Rectangle:
    """Rectangle class docstring."""
    width: float
    height: float

    def area(self) -> float:
        """area method docstring."""
        return self.width * self.height

rect = Rectangle(10, 5)
print(rect.area())  # 50.0
```

**Q22: How do you exclude fields from `__init__` in dataclasses?**
A: Use `field(init=False)` and set the value in `__post_init__`.

```python
from dataclasses import dataclass, field

@dataclass
class User:
    """User class docstring."""
    name: str
    age: int
    full_name: str = field(init=False)

    def __post_init__(self) -> None:
        """__post_init__ method docstring."""
        self.full_name = f"Mr. {self.name}"

user = User("Alice", 30)
print(user.full_name)  # Mr. Alice
```

**Q23: Can dataclasses inherit from other dataclasses?**
A: Yes, child dataclasses inherit fields from parents. Parent fields appear first in the constructor.

```python
@dataclass
class Person:
    """Person class docstring."""
    name: str
    age: int

@dataclass
class Employee(Person):
    """Employee class docstring."""
    employee_id: int

emp = Employee("Alice", 30, 1001)
print(emp)  # Employee(name='Alice', age=30, employee_id=1001)
```

**Q24: How do you compare dataclasses for equality?**
A: `__eq__` is auto-generated, comparing all fields. Use `@dataclass(order=True)` for `<`, `>`, etc.

```python
@dataclass(order=True)
class User:
    """User class docstring."""
    name: str
    age: int

u1 = User("Alice", 30)
u2 = User("Alice", 30)
print(u1 == u2)  # True
```

**Q25: What's the performance difference between dataclasses and Pydantic?**
A: Dataclasses are faster — no validation overhead. Pydantic validates at runtime and serialises, but adds 10–100µs per model construction. Use dataclasses for internal data structures that never cross API or process boundaries; Pydantic at API boundaries.

**Q26: How do you make a dataclass hashable?**
A: Use `@dataclass(frozen=True)` to make it immutable, which enables hashing.

```python
@dataclass(frozen=True)
class Point:
    """Point class docstring."""
    x: int
    y: int

points = {Point(1, 2), Point(3, 4)}  # Can use as dict keys or in sets
```

**Q27: What's `__post_init__` used for in dataclasses?**
A: Runs after `__init__`. Use for validation, computed fields, or side effects that require all fields to be set first.

```python
@dataclass
class User:
    """User class docstring."""
    name: str
    age: int

    def __post_init__(self) -> None:
        """__post_init__ method docstring."""
        if self.age < 0:
            raise ValueError("Age cannot be negative")

user = User("Alice", 30)  # OK
# User("Bob", -5)  # Raises ValueError
```

**Q28: Can you exclude fields from repr in dataclasses?**
A: Yes, use `field(repr=False)`.

```python
@dataclass
class User:
    """User class docstring."""
    name: str
    password: str = field(repr=False)  # Never printed

user = User("Alice", "secret123")
print(user)  # User(name='Alice')  — password not shown
```

**Q29: How do you handle optional fields in dataclasses?**
A: Use `T | None` with default `None`.

```python
@dataclass
class User:
    """User class docstring."""
    name: str
    email: str | None = None

u1 = User("Alice")
u2 = User("Bob", "bob@example.com")
```

**Q30: What's the TypeScript equivalent of a dataclass?**
A: TypeScript class with constructor property shorthand, or a plain interface with a factory function.

```typescript
// TypeScript equivalent of a Python dataclass
class User {
  constructor(
    public name: string,
    public age: number,
    public email: string,
  ) {}
}
```

---

### 🎯 Working Code Artefact 2: Dataclasses in Practice

```python
"""
Dataclasses: Production patterns for Python data modelling
Similar to TypeScript classes with constructor property shorthand
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum


# 1. Basic dataclass
@dataclass
class User:
    """Simple user model."""
    name: str
    age: int
    email: str


# 2. Dataclass with defaults
@dataclass
class Config:
    """Configuration with default values."""
    debug: bool = False
    max_retries: int = 3
    timeout: float = 30.0


# 3. Dataclass with mutable defaults
@dataclass
class Project:
    """Project with tags list (mutable default)."""
    name: str
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)


# 4. Frozen (immutable) dataclass
@dataclass(frozen=True)
class Point:
    """Immutable 2D point — hashable, usable in sets and as dict keys."""
    x: float
    y: float

    def distance_from_origin(self) -> float:
        """distance_from_origin method docstring."""
        return (self.x ** 2 + self.y ** 2) ** 0.5


# 5. Dataclass with computed fields
@dataclass
class Person:
    """Person with computed full name."""
    first_name: str
    last_name: str
    full_name: str = field(init=False)

    def __post_init__(self) -> None:
        """__post_init__ method docstring."""
        self.full_name = f"{self.first_name} {self.last_name}"


# 6. Dataclass with validation
@dataclass
class Product:
    """Product with price validation."""
    name: str
    price: float
    quantity: int

    def __post_init__(self) -> None:
        """__post_init__ method docstring."""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")


# 7. Dataclass inheritance
@dataclass
class Employee(Person):
    """Employee extends Person."""
    employee_id: int
    department: str


# 8. Dataclass with enum
class Status(Enum):
    """Status class docstring."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class Ticket:
    """Support ticket with status enum."""
    id: int
    title: str
    status: Status = Status.PENDING


# 9. Dataclass with optional fields
@dataclass
class Article:
    """Article with optional metadata."""
    title: str
    content: str
    author: str
    published_at: datetime | None = None
    updated_at: datetime | None = None


# 10. Dataclass with order comparison
@dataclass(order=True)
class Priority:
    """Priority item with ordering."""
    level: int
    name: str = field(compare=False)  # excluded from comparison


# 11. Dataclass with hidden fields in repr
@dataclass
class SecureUser:
    """User with sensitive fields hidden from repr."""
    username: str
    password: str = field(repr=False)
    api_key: str = field(repr=False)


# 12. Nested dataclasses
@dataclass
class Address:
    """Address class docstring."""
    street: str
    city: str
    country: str


@dataclass
class Company:
    """Company with nested address."""
    name: str
    address: Address
    employees: list[Employee] = field(default_factory=list)


if __name__ == "__main__":
    """Only run this block of code if I am executing this file directly. 
    Do not run it if I am just importing this file into another script"""

    user = User("Alice", 30, "alice@example.com")
    print(user)
    print(asdict(user))

    config = Config(debug=True)
    print(config)

    project = Project("My App")
    project.tags.append("python")
    project.tags.append("fastapi")
    print(project)

    point = Point(3.0, 4.0)
    print(f"Distance: {point.distance_from_origin()}")

    person = Person("John", "Doe")
    print(person.full_name)  # John Doe

    try:
        Product("Widget", -10, 5)
    except ValueError as e:
        print(f"Validation error: {e}")

    emp = Employee("Jane", "Smith", 1001, "Engineering")
    print(emp.full_name)
    print(emp.employee_id)

    ticket = Ticket(1, "Bug fix")
    print(ticket.status)

    address = Address("123 Main St", "London", "UK")
    company = Company("Tech Corp", address)
    company.employees.append(emp)
    print(asdict(company))
```

### ✅ Key Concepts

- **Dataclasses reduce boilerplate**: Auto-generate `__init__`, `__repr__`, `__eq__`
- **Use `field()` for advanced options**: `default_factory`, `repr=False`, `init=False`
- **`__post_init__` for validation**: Runs after initialisation, perfect for computed fields
- **Frozen dataclasses are hashable**: Can use as dict keys or in sets

### ⚠️ Common Pitfalls

- Using mutable defaults (`list`, `dict`) without `field(default_factory=...)` — shared between all instances
- Forgetting that dataclasses are mutable by default (use `frozen=True` for immutability)
- Over-using dataclasses for behaviour-heavy classes (use regular classes instead)

---

## 🖥️ Part 3: Pydantic v2 Models (Runtime Validation)

### Q&A Batch 3: Pydantic v2

**Q31: What's the difference between dataclasses and Pydantic models?**
A: Pydantic validates data at runtime and handles serialisation/deserialisation. Dataclasses are faster but have no validation. Use Pydantic for API boundaries; dataclasses internally.

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    """User class docstring."""
    name: str
    age: int
    email: EmailStr  # validates email format at runtime

user = User(name="Alice", age=30, email="alice@example.com")
# User(name="Bob", age=-5, email="invalid")  # raises ValidationError
```

**Q32: How do you define a Pydantic v2 model?**
A: Inherit from `BaseModel` and use type annotations. Validation happens automatically on instantiation.

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    """Product class docstring."""
    name: str
    price: float = Field(gt=0)   # must be > 0
    quantity: int = Field(ge=0)  # must be >= 0

product = Product(name="Widget", price=9.99, quantity=10)
```

**Q33: What's `Field()` used for in Pydantic?**
A: Add validation rules, defaults, descriptions, examples. Similar to decorators in class-validator (TS).

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    """User class docstring."""
    name: str = Field(min_length=1, max_length=50)
    age: int = Field(ge=0, le=150)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
```

**Q34: How do you handle optional fields in Pydantic?**
A: Use `T | None` with default `None`.

```python
class User(BaseModel):
    """User class docstring."""
    name: str
    email: str | None = None
    phone: str | None = None

user = User(name="Alice")  # email and phone default to None
```

**Q35: How do you serialise Pydantic models to JSON?**
A: Use `.model_dump()` (v2) or `.model_dump_json()` for a JSON string. Never use the v1 `.dict()` — it is removed in v2.

```python
class User(BaseModel):
    """User class docstring."""
    name: str
    age: int

user = User(name="Alice", age=30)
print(user.model_dump())       # {'name': 'Alice', 'age': 30}
print(user.model_dump_json())  # '{"name":"Alice","age":30}'
```

**Q36: How do you parse JSON into Pydantic models?**
A: Use `.model_validate()` (v2) or `.model_validate_json()` for JSON strings.

```python
data = {"name": "Alice", "age": 30}
user = User.model_validate(data)

json_str = '{"name": "Bob", "age": 25}'
user2 = User.model_validate_json(json_str)
```

**Q37: What are Pydantic v2's major improvements over v1?**
A: 5–50× faster (Rust core), better error messages, stricter validation by default, new `model_*` methods replacing `.dict()` and `.json()`, computed fields with `@computed_field`.

```python
from pydantic import BaseModel, computed_field

class User(BaseModel):
    """User class docstring."""
    first_name: str
    last_name: str

    @computed_field   # v2 feature
    @property
    def full_name(self) -> str:
        """full_name method docstring."""
        return f"{self.first_name} {self.last_name}"

user = User(first_name="Alice", last_name="Smith")
print(user.full_name)  # Alice Smith
```

**Q38: How do you add custom validators in Pydantic v2?**
A: Use `@field_validator` decorator (replaces v1's `@validator`).

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    """User class docstring."""
    name: str
    age: int

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        """validate_age method docstring."""
        if v < 0:
            raise ValueError("Age cannot be negative")
        return v
```

**Q39: How do you validate across multiple fields in Pydantic?**
A: Use `@model_validator(mode="after")`.

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    """DateRange class docstring."""
    start_date: str
    end_date: str

    @model_validator(mode="after")
    def validate_date_range(self) -> "DateRange":
        """validate_date_range method docstring."""
        if self.start_date > self.end_date:
            raise ValueError("start_date must be before end_date")
        return self
```

**Q40: How do you handle nested Pydantic models?**
A: Reference other models as field types. Validation is recursive.

```python
class Address(BaseModel):
    """Address class docstring."""
    street: str
    city: str

class User(BaseModel):
    """User class docstring."""
    name: str
    address: Address

user = User(name="Alice", address={"street": "123 Main St", "city": "London"})
print(user.address.city)  # London
```

**Q41: How do you exclude fields from serialisation in Pydantic?**
A: Use `exclude=True` in `Field()` or pass `exclude` to `.model_dump()`.

```python
class User(BaseModel):
    """User class docstring."""
    name: str
    password: str = Field(exclude=True)

user = User(name="Alice", password="secret")
print(user.model_dump())  # {'name': 'Alice'} — password excluded
```

**Q42: What's `ConfigDict` in Pydantic v2?**
A: Replaces v1's inner `class Config`. Configure validation behaviour, aliases, ORM mode, etc.

```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    """User class docstring."""
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        from_attributes=True,  # required when reading from SQLAlchemy ORM objects (Day 3)
    )

    name: str
    age: int

user = User(name="  Alice  ", age=30)
print(user.name)  # "Alice" (whitespace stripped)
```

**Q43: How do you handle extra fields in Pydantic?**
A: Use `model_config = ConfigDict(extra="forbid")` to reject, `"allow"` to keep, or `"ignore"` (default) to discard.

```python
class User(BaseModel):
    """User class docstring."""
    model_config = ConfigDict(extra="forbid")

    name: str
    age: int

# User(name="Alice", age=30, email="a@b.com")  # ValidationError: extra fields
```

**Q44: How do you use Pydantic with environment variables?**
A: Use `pydantic-settings` and `BaseSettings`. Use `model_config = {"env_file": ".env"}` — the `class Config` inner class was deprecated in v2.

```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Settings class docstring."""
    database_url: str
    secret_key: str
    debug: bool = False

    # 2026 style — dict shorthand, not inner class Config
    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    """get_settings function docstring."""
    return Settings()  # parses .env once per process

settings = get_settings()
```

**Q45: What's `SecretStr` and when should you use it?**
A: `SecretStr` is a Pydantic type that stores a string securely — it renders as `'**********'` in `repr()`, logs, and `model_dump()`. The actual value is only accessible via `.get_secret_value()`. Use it for any password, API key, or token field to prevent accidental logging.

```python
from pydantic import BaseModel, SecretStr

class UserCreate(BaseModel):
    """UserCreate class docstring."""
    email: str
    password: SecretStr  # never appears in logs, repr, or model_dump()

user = UserCreate(email="a@b.com", password="secret123")
print(user)              # email='a@b.com' password=SecretStr('**********')
print(user.model_dump()) # {'email': 'a@b.com', 'password': SecretStr('**********')}

# Access the real value only when needed (e.g., hashing)
raw = user.password.get_secret_value()  # "secret123"
```

---

### 🎯 Working Code Artefact 3: Pydantic v2 Production Patterns

```python
"""
Pydantic v2: Production patterns for FastAPI and data validation
Runtime validation + serialisation in one package
"""

from datetime import datetime
from enum import Enum
from typing import Annotated
from pydantic import (
    BaseModel, Field, EmailStr, HttpUrl, ConfigDict, SecretStr,
    field_validator, model_validator, computed_field
)

# 1. Basic model with validation
class User(BaseModel):
    """User model with email validation."""
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=150)
    email: EmailStr  # validates email format

# 2. Model with custom validators
class Product(BaseModel):
    """Product with custom validation logic."""
    name: str
    price: float
    sku: str

    @field_validator("price")
    @classmethod
    def validate_price(cls, v: float) -> float:
        """validate_price method docstring."""
        if v <= 0:
            raise ValueError("Price must be positive")
        return round(v, 2)  # round to 2 decimal places

    @field_validator("sku")
    @classmethod
    def validate_sku(cls, v: str) -> str:
        """validate_sku method docstring."""
        if not v.startswith("SKU-"):
            raise ValueError("SKU must start with 'SKU-'")
        return v.upper()

# 3. Model with computed fields
class Person(BaseModel):
    """Person with computed full name."""
    first_name: str
    last_name: str

    @computed_field
    @property
    def full_name(self) -> str:
        """full_name method docstring."""
        return f"{self.first_name} {self.last_name}"

# 4. Model with model validator (cross-field validation)
class DateRange(BaseModel):
    """Date range with cross-field validation."""
    start_date: datetime
    end_date: datetime

    @model_validator(mode="after")
    def validate_dates(self) -> "DateRange":
        """validate_dates method docstring."""
        if self.start_date >= self.end_date:
            raise ValueError("start_date must be before end_date")
        return self

# 5. Nested models
class Address(BaseModel):
    """Address class docstring."""
    street: str
    city: str
    country: str
    postal_code: str

class Company(BaseModel):
    """Company with nested address."""
    name: str
    website: HttpUrl
    address: Address
    employees: list[User] = Field(default_factory=list)

# 6. Model with enums
class OrderStatus(str, Enum):
    """OrderStatus class docstring."""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class Order(BaseModel):
    """Order class docstring."""
    id: int
    status: OrderStatus = OrderStatus.PENDING
    items: list[Product]
    total: float = Field(gt=0)

# 7. Model with optional fields
class Article(BaseModel):
    """Article class docstring."""
    title: str
    content: str
    author: str
    published_at: datetime | None = None
    tags: list[str] = Field(default_factory=list)
    view_count: int = 0

# 8. Model with aliases (camelCase from frontend → snake_case in Python)
class ApiResponse(BaseModel):
    """ApiResponse class docstring."""
    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(alias="userId")
    created_at: datetime = Field(alias="createdAt")
    is_active: bool = Field(alias="isActive")

# 9. Model that forbids extra fields
class StrictUser(BaseModel):
    """StrictUser class docstring."""
    model_config = ConfigDict(extra="forbid")

    name: str
    email: EmailStr

# 10. Frozen (immutable) model
class AppConfig(BaseModel):
    """AppConfig class docstring."""
    model_config = ConfigDict(frozen=True)

    api_key: SecretStr   # never logs the key value
    base_url: HttpUrl
    timeout: int = 30

# 11. ORM-compatible response schema (used from Day 3 onwards with SQLAlchemy)
class UserResponse(BaseModel):
    """Safe output schema — excludes write-only fields."""
    id: int
    name: str
    email: str
    model_config = ConfigDict(from_attributes=True)  # required for SQLAlchemy ORM objects

# 12. Request schema with SecretStr
class UserCreate(BaseModel):
    """Input schema — password never leaks into logs or responses."""
    name: str
    email: EmailStr
    password: SecretStr  # access via .get_secret_value() only at hash time

# 13. Generic API result wrapper
class ApiResult(BaseModel):
    """ApiResult class docstring."""
    success: bool
    message: str
    data: dict | list | None = None
    errors: list[str] = Field(default_factory=list)


if __name__ == "__main__":
    """Only run this block of code if I am executing this file directly. 
    Do not run it if I am just importing this file into another script"""
    
    # Basic validation
    user = User(name="Alice", age=30, email="alice@example.com")
    print(user.model_dump())

    # Custom validators
    product = Product(name="Widget", price=19.999, sku="sku-12345")
    print(product.price)  # 20.0 (rounded)
    print(product.sku)    # SKU-12345 (uppercased)

    # Computed fields
    person = Person(first_name="John", last_name="Doe")
    print(person.full_name)       # John Doe
    print(person.model_dump())    # includes full_name

    # Cross-field validation
    date_range = DateRange(
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 12, 31)
    )
    print(date_range)

    # Nested models
    address = Address(street="123 Main St", city="London",
                      country="UK", postal_code="SW1A 1AA")
    company = Company(name="Tech Corp", website="https://techcorp.com", address=address)
    print(company.model_dump_json(indent=2))

    # Aliases
    api_data = {"userId": 123, "createdAt": "2026-04-21T10:00:00", "isActive": True}
    api_response = ApiResponse.model_validate(api_data)
    print(api_response.user_id)  # 123

    # SecretStr — password never appears in output
    new_user = UserCreate(name="Alice", email="a@b.com", password="secret123")
    print(new_user)              # password=SecretStr('**********')
    print(new_user.model_dump()) # password appears masked
    raw = new_user.password.get_secret_value()  # only access point for raw value
    print(f"Would hash: {raw[:3]}***")
```

### ✅ Key Concepts

- **Pydantic validates at runtime**: Unlike type hints, Pydantic catches errors when data is assigned
- **Use for API boundaries**: FastAPI uses Pydantic for request/response validation automatically
- **v2 is 5–50× faster**: Rust-based core — always use `pydantic >= 2.0`
- **`model_config = ConfigDict(from_attributes=True)`** is required for response schemas that read from SQLAlchemy ORM objects (introduced Day 3)
- **`SecretStr` for all password and token fields** — prevents accidental logging
- **`class Config:` is v1 legacy** — use `model_config = {"env_file": ".env"}` or `ConfigDict(...)` in all new code

### ⚠️ Common Pitfalls

- Using Pydantic everywhere (overkill; use dataclasses internally)
- Calling `.dict()` or `.json()` — these are v1 methods, removed in v2; use `.model_dump()` and `.model_dump_json()`
- Using `class Config:` inner class — deprecated in Pydantic v2; use `model_config = ConfigDict(...)`
- Forgetting `from_attributes=True` on response schemas that map from SQLAlchemy models (Day 3)
- Not using `SecretStr` for passwords — they appear in logs and tracebacks as plain text

---

## 🖥️ Part 4: Async/Await Patterns

### Q&A Batch 4: Async/Await

**Q46: How does Python's async/await compare to JavaScript?**
A: Very similar syntax. Python has an explicit event loop (`asyncio`). JS runs the event loop automatically. Both are single-threaded, cooperative multitasking — only one coroutine runs at a time; others yield at `await` points.

```python
import asyncio

async def fetch_data() -> str:
    await asyncio.sleep(1)  # like setTimeout but awaitable
    return "Data"

result = asyncio.run(fetch_data())
```

**Q47: What's the Python equivalent of `Promise`?**
A: A `coroutine` (async function) or `asyncio.Task`. Use `await` to get the result.

```python
async def async_function() -> str:
    await asyncio.sleep(1)
    return "Done"

async def main() -> None:
    result = await async_function()
    print(result)

asyncio.run(main())
```

**Q48: How do you run multiple async tasks concurrently?**
A: Use `asyncio.gather()` (like `Promise.all()`) or `asyncio.create_task()`.

```python
async def task1() -> str:
    await asyncio.sleep(1)
    return "Task 1"

async def task2() -> str:
    await asyncio.sleep(1)
    return "Task 2"

async def main() -> None:
    # Both run concurrently — total time ~1s, not 2s
    results = await asyncio.gather(task1(), task2())
    print(results)  # ['Task 1', 'Task 2']

asyncio.run(main())
```

**Q49: What's `asyncio.create_task()` used for?**
A: Schedule a coroutine to run concurrently. Returns a `Task` that can be awaited later.

```python
async def background_task() -> None:
    await asyncio.sleep(2)
    print("Background task done")

async def main() -> None:
    task = asyncio.create_task(background_task())  # starts immediately
    print("Main function continues")
    await task  # wait for completion

asyncio.run(main())
```

**Q50: How do you handle async exceptions?**
A: Use try/except around `await` statements — works identically to sync exceptions.

```python
async def failing_task() -> None:
    await asyncio.sleep(1)
    raise ValueError("Something went wrong")

async def main() -> None:
    try:
        await failing_task()
    except ValueError as e:
        print(f"Caught error: {e}")

asyncio.run(main())
```

**Q51: What's the Python equivalent of `Promise.race()`?**
A: `asyncio.wait()` with `return_when=asyncio.FIRST_COMPLETED`.

```python
async def main() -> None:
    tasks = [asyncio.create_task(task1()), asyncio.create_task(task2())]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    for task in done:
        print(f"First done: {task.result()}")

    for task in pending:
        task.cancel()  # always cancel remaining tasks to avoid resource leaks
```

**Q51.1 What is a deterministic FastAPI endpoint?**
A: It is an endpoint that guarantees the exact same response for the exact same request every time. Think of a standard GET /items/5 route pulling from a static database—it is 100% predictable, easily testable, and safe to cache.

**Q51.2: How does stochastic behavior work in an asyncio context?**
A: It introduces randomness into your code, meaning outcomes or execution paths will vary even with the same input. A common example is using await asyncio.sleep(random.uniform(0.1, 1.0)) to add an unpredictable delay (jitter) to prevent simultaneous server reconnects.

**Q52: How do you use async context managers?**
A: Use `async with` for resources that require async setup/teardown. Define `__aenter__` and `__aexit__`.

```python
class AsyncResource:
    """AsyncResource class docstring."""
    async def __aenter__(self) -> "AsyncResource":
        await asyncio.sleep(0.1)  # simulate async acquisition
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await asyncio.sleep(0.1)  # simulate async release

async def main() -> None:
    async with AsyncResource() as resource:
        print("Using resource")
```

**Q53: What's the difference between `await` and `asyncio.run()`?**
A: `await` is used inside async functions. `asyncio.run()` is the entry point from synchronous code — it creates and runs an event loop.

```python
async def async_func() -> str:
    return "Result"

# From sync code (entry point)
result = asyncio.run(async_func())

# Inside async code
async def another_async() -> str:
    result = await async_func()  # always await inside async functions
    return result
```

**Q54: How do you convert blocking I/O to async?**
A: Use `asyncio.to_thread()` (Python 3.9+) to run blocking code in a thread pool.

```python
import time

def blocking_io() -> str:
    """blocking_io function docstring."""
    time.sleep(1)  # blocks the thread
    return "Done"

async def main() -> None:
    result = await asyncio.to_thread(blocking_io)  # runs in thread pool — event loop free
    print(result)
```

**Q55: What's an async generator?**
A: A function with `yield` inside `async def`. Use `async for` to consume. Like async iterables in TypeScript.

```python
async def async_range(n: int):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

async def main() -> None:
    async for value in async_range(5):
        print(value)
```

**Q56: How do you handle timeouts in async code?**
A: Use `asyncio.wait_for()` with a timeout value.

```python
async def slow_task() -> str:
    await asyncio.sleep(5)
    return "Done"

async def main() -> None:
    try:
        result = await asyncio.wait_for(slow_task(), timeout=2.0)
    except asyncio.TimeoutError:
        print("Task timed out")
```

**Q57: What's the GIL and how does it affect async code?**
A: The Global Interpreter Lock (GIL) limits CPython to executing one Python bytecode instruction at a time across all threads. Async I/O (network, disk) is not affected because the event loop yields while waiting — no bytecode executes during I/O waits. CPU-bound tasks (image processing, ML inference) do contend for the GIL — use `ProcessPoolExecutor` for those. Python 3.14 supports free-threaded builds (PEP 703), removing the GIL for CPU-bound workloads. Free-threaded mode is still evolving and not universally adopted across all third-party libraries; multiprocessing remains the safe default for CPU-bound work until the ecosystem fully matures.

**Q58: Can you mix async and sync code?**
A: Yes — but never call blocking sync functions directly in `async def` routes (blocks the entire event loop). Wrap them with `asyncio.to_thread()`.

**Q59: How do you cancel async tasks?**
A: Call `.cancel()` on the task. It raises `asyncio.CancelledError` inside the task at the next `await` point.

```python
async def long_task() -> None:
    try:
        await asyncio.sleep(10)
    except asyncio.CancelledError:
        print("Task was cancelled — cleanup here")
        raise  # always re-raise CancelledError

async def main() -> None:
    task = asyncio.create_task(long_task())
    await asyncio.sleep(1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Caught cancellation in main")
```

**Q60: What are common async patterns in FastAPI?**
A: Async route handlers, async database queries (SQLAlchemy async — Day 3), concurrent external API calls with `asyncio.gather()`, background tasks (Day 2), SSE streaming responses.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int) -> dict:
    # Concurrent async operations
    profile, posts = await asyncio.gather(
        fetch_profile(user_id),
        fetch_posts(user_id)
    )
    return {"profile": profile, "posts": posts}
```

---

### 🎯 Working Code Artefact 4: Async/Await Production Patterns

```python
"""
Async/Await: Production patterns for FastAPI and concurrent operations
Mental model mapping from TypeScript/Node.js to Python asyncio
"""

import asyncio
from typing import Any
from contextlib import asynccontextmanager


# 1. Basic async function
async def fetch_data(url: str) -> dict[str, str]:
    """Simulate API call."""
    await asyncio.sleep(0.5)
    return {"url": url, "data": "some data"}


# 2. Concurrent execution (like Promise.all)
async def fetch_multiple_concurrent() -> list[dict[str, str]]:
    urls = ["api.com/1", "api.com/2", "api.com/3"]
    return list(await asyncio.gather(*[fetch_data(url) for url in urls]))


# 3. Sequential vs concurrent timing
async def sequential_execution() -> list[dict[str, str]]:
    """Sequential: ~1.5 seconds total."""
    r1 = await fetch_data("api.com/1")
    r2 = await fetch_data("api.com/2")
    r3 = await fetch_data("api.com/3")
    return [r1, r2, r3]


async def concurrent_execution() -> list[Any]:
    """Concurrent: ~0.5 seconds total."""
    return list(await asyncio.gather(
        fetch_data("api.com/1"),
        fetch_data("api.com/2"),
        fetch_data("api.com/3"),
    ))


# 4. Error handling
async def fetch_with_error_handling(url: str) -> dict[str, str] | None:
    try:
        return await fetch_data(url)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


# 5. Timeout handling
async def fetch_with_timeout(url: str, timeout: float = 2.0) -> dict[str, str]:
    try:
        return await asyncio.wait_for(fetch_data(url), timeout=timeout)
    except asyncio.TimeoutError:
        return {"error": "Request timed out"}


# 6. Race — first completed wins (like Promise.race)
async def fetch_fastest() -> Any:
    tasks = [
        asyncio.create_task(fetch_data("fast-api.com")),
        asyncio.create_task(fetch_data("slow-api.com")),
    ]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()
    return list(done)[0].result()


# 7. Async context manager (like using...dispose in TS)
class AsyncDatabaseConnection:
    """AsyncDatabaseConnection class docstring."""
    async def __aenter__(self) -> "AsyncDatabaseConnection":
        print("Opening database connection")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        print("Closing database connection")
        await asyncio.sleep(0.1)

    async def query(self, sql: str) -> list[dict[str, Any]]:
        await asyncio.sleep(0.2)
        return [{"id": 1, "name": "Alice"}]


async def use_database() -> list[dict[str, Any]]:
    async with AsyncDatabaseConnection() as db:
        return await db.query("SELECT * FROM users")


# 8. Semaphore for rate limiting
async def fetch_with_rate_limit(urls: list[str], max_concurrent: int = 3) -> list[Any]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_limited(url: str) -> dict[str, str]:
        async with semaphore:
            return await fetch_data(url)

    return list(await asyncio.gather(*[fetch_limited(url) for url in urls]))


# 9. Retry with exponential backoff
async def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> dict[str, str]:
    for attempt in range(max_retries):
        try:
            return await fetch_data(url)
        except Exception:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Retry {attempt + 1}/{max_retries} after {delay}s")
            await asyncio.sleep(delay)
    return {}


# 10. Async generator — paginated data stream
async def fetch_paginated_data(pages: int):
    for page in range(1, pages + 1):
        await asyncio.sleep(0.3)
        yield {"page": page, "data": f"Page {page} data"}

async def background_task(name: str, delay: float):
    """Simulated background task"""
    await asyncio.sleep(delay)
    print(f"Background task {name} completed")

async def main_with_background():
    """Start background task without waiting"""
    task = asyncio.create_task(background_task("cleanup", 2.0))
    print("Main function continues immediately")
    # Don't await - task runs in background
    await asyncio.sleep(0.5)
    print("Main function done (background still running)")
    await task  # Optional: wait for background task

async def consume_paginated() -> list[dict[str, Any]]:
    results = []
    async for page_data in fetch_paginated_data(3):
        results.append(page_data)
    return results


# 11. Task cancellation
async def cancellable_task() -> None:
    try:
        await asyncio.sleep(5)
    except asyncio.CancelledError:
        print("Task was cancelled — cleanup here")
        raise  # always re-raise

async def cancel_task_example():
    """Cancel a running task"""
    task = asyncio.create_task(cancellable_task())
    await asyncio.sleep(1)
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("Caught cancellation in main")

# 12. Producer-consumer with async queue
async def producer_consumer_pattern() -> None:
    queue: asyncio.Queue[int | None] = asyncio.Queue(maxsize=5)

    async def producer() -> None:
        for i in range(10):
            await asyncio.sleep(0.1)
            await queue.put(i)
        await queue.put(None)  # sentinel

    async def consumer() -> None:
        while True:
            item = await queue.get()
            if item is None:
                break
            await asyncio.sleep(0.15)
            print(f"Consumed: {item}")

    await asyncio.gather(producer(), consumer())


# Main execution examples
async def run_examples():
    """Run all examples"""

    print("\n1. Basic async:")
    result = await fetch_data("example.com")
    print(result)

    print("\n2. Concurrent execution:")
    results = await fetch_multiple_concurrent()
    print(f"Fetched {len(results)} results concurrently")

    print("\n3. Sequential vs Concurrent timing:")
    import time

    start = time.time()
    await sequential_execution()
    seq_time = time.time() - start

    start = time.time()
    await concurrent_execution()
    conc_time = time.time() - start

    print(f"Sequential: {seq_time:.2f}s, Concurrent: {conc_time:.2f}s")

    print("\n4. Error handling:")
    await fetch_with_error_handling("error-api.com")

    print("\n5. Timeout:")
    result = await fetch_with_timeout("slow-api.com", timeout=1.0)
    print(result)

    print("\n6. Race (fastest wins):")
    fastest = await fetch_fastest()
    print(fastest)

    print("\n7. Async context manager:")
    db_results = await use_database()
    print(db_results)

    print("\n8. Background task:")
    await main_with_background()

    print("\n9. Async generator:")
    await consume_paginated()

    print("\n10. Rate limiting:")
    urls = [f"api.com/{i}" for i in range(10)]
    limited_results = await fetch_with_rate_limit(urls, max_concurrent=3)
    print(f"Fetched {len(limited_results)} with rate limit")

    print("\n11. Retry logic:")
    retry_result = await fetch_with_retry("unreliable-api.com")
    print(retry_result)

    print("\n12. Task cancellation:")
    await cancel_task_example()

    print("\n13. Producer-consumer:")
    await producer_consumer_pattern()


if __name__ == "__main__":
    # Entry point from sync code (like top-level await)
    asyncio.run(run_examples())
```

### ✅ Key Concepts

- **`asyncio.run()` is the entry point**: Use from sync code (like top-level await in TS modules)
- **`asyncio.gather()` for concurrent execution**: Like `Promise.all()` — runs tasks concurrently, not sequentially
- **Use `async with` for resources**: Database connections, file handles, HTTP clients
- **Never block the event loop**: Use `asyncio.to_thread()` for any blocking I/O in async routes

### ⚠️ Common Pitfalls

- Calling blocking sync functions directly in `async def` routes — blocks the entire event loop for all concurrent requests
- Forgetting to `await` async functions — returns a coroutine object, not the result; silent bug
- Using `time.sleep()` instead of `asyncio.sleep()` inside async functions — blocks the event loop
- Not cancelling pending tasks after `asyncio.wait()` — resource and memory leaks

---

## 🖥️ Part 5: Python Tooling Setup

### Q&A Batch 5: Tooling

**Q61: What is `uv` and why is it the 2026 default?**
A: `uv` is a Rust-based all-in-one Python toolchain — it replaces `pyenv` (version management), `venv` (virtual environments), and `pip`/`poetry` (dependency management) in a single binary. It is 10–100× faster than equivalent Python-based tools. Senior engineers use `uv` for all new projects in 2026.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Manage Python versions (replaces pyenv)
uv python install 3.14
uv python pin 3.14       # writes .python-version
uv python list           # show available versions

# Create and manage a project
uv init my-project
cd my-project
uv add fastapi pydantic
uv add --dev ruff mypy pytest

# Run commands inside the managed venv
uv run python main.py
uv run pytest
uv run mypy .
uv run ruff check .

# Sync all dependencies from lockfile
uv sync
```

> **pyenv (legacy):** `pyenv` was the pre-2026 standard for Python version management. With `uv python install` covering the same need, `pyenv` is no longer required for new projects. You may still encounter it in existing codebases and CI configs — it is not wrong to know it, but do not set it up by default.

**Q62: What's `poetry` and when do you still use it?**
A: `poetry` is a mature dependency manager with a lockfile, virtual env management, and a rich plugin ecosystem. It remains common in existing codebases and is frequently asked about in interviews. Senior engineers know both `uv` and `poetry`.

```bash
# --- Using poetry (common in existing codebases) ---
# Create project
poetry new my-project
cd my-project

# Add dependencies
poetry add "fastapi[standard]" pydantic pydantic-settings

# Add dev dependencies
poetry add --group dev pytest ruff mypy pytest-asyncio httpx

# Install all dependencies
poetry install

# Run in virtual environment
poetry run python main.py
poetry run pytest
```

> Use `uv` for new greenfield projects. Use `poetry` when joining an existing codebase that already uses it, or when a team has established tooling around it. Both produce a lockfile and deterministic builds.

**Q63: What's `ruff` and why is it the new standard?**
A: Rust-based linter + formatter, 100× faster than pylint/flake8/black. Replaces 5+ tools in a single binary. Default in 2026.

```bash
# --- Using uv (recommended) ---
uv run ruff check .
uv run ruff check --fix .
uv run ruff format .

# --- Using poetry (existing codebases) ---
poetry run ruff check .
poetry run ruff check --fix .
poetry run ruff format .
```

```toml
[tool.ruff]
line-length = 100
target-version = "py314"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]  # errors, flake8, isort, naming, warnings, pyupgrade
```

**Q64: What's `mypy` and how do you configure it?**
A: Static type checker. Runs type analysis on your code. Essential for production Python — equivalent to `tsc --noEmit` in TypeScript.

```bash
# --- Using uv (recommended) ---
uv run mypy .

# --- Using poetry (existing codebases) ---
poetry run mypy .
```

```toml
[tool.mypy]
python_version = "3.14"
strict = true
warn_return_any = true
disallow_untyped_defs = true
```

**Q65: How do you set up VS Code for Python?**
A: Install the Python and Ruff extensions, configure settings for auto-format on save.

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.typeCheckingMode": "strict",

  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },

  "ruff.lint.enable": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false
}
```

**Q66: What's the Python equivalent of `package.json` scripts?**
A: `uv run` commands (or `poetry run` in existing codebases) combined with a `Makefile` for common tasks.

```makefile
# Makefile — uv-based (recommended for new projects)
.PHONY: install lint format test dev prod

install:
	uv sync

lint:
	uv run ruff check .
	uv run mypy .

format:
	uv run ruff format .
	uv run ruff check --fix .

test:
	uv run pytest --cov=. --cov-report=term-missing

dev:
	uv run fastapi dev main.py      # development: hot reload

prod:
	uv run fastapi run main.py      # production: no reload
```

```makefile
# Makefile — poetry-based (for existing codebases)
.PHONY: install lint format test dev prod

install:
	poetry install

lint:
	poetry run ruff check .
	poetry run mypy .

format:
	poetry run ruff format .
	poetry run ruff check --fix .

test:
	poetry run pytest --cov=. --cov-report=term-missing

dev:
	poetry run fastapi dev main.py   # development: hot reload

prod:
	poetry run fastapi run main.py   # production: no reload
```

**Q67: How do you structure a Python project?**
A: Standard structure with package directory at root, tests alongside, config in `pyproject.toml`.

```
my-project/
├── pyproject.toml
├── uv.lock            # uv lockfile (or poetry.lock if using poetry)
├── README.md
├── .python-version    # written by `uv python pin` or `pyenv local`
├── .gitignore
├── my_project/          # main package
│   ├── __init__.py
│   ├── main.py
│   └── models.py
└── tests/
    ├── __init__.py
    ├── conftest.py      # shared fixtures
    └── test_main.py
```

**Q68: What goes in `pyproject.toml`?**
A: Project metadata, dependencies, and all tool configurations (ruff, mypy, pytest). Like `package.json` + ESLint config + Jest config combined into one file. The format is the same for both `uv` and `poetry` projects; only the `[project]` / `[tool.poetry]` sections differ.

```toml
# --- uv-managed project (recommended) ---
[project]
name = "my-project"
version = "0.1.0"
description = "My FastAPI project"
requires-python = ">=3.14"
dependencies = [
    "fastapi[standard]>=0.120",
    "pydantic>=2.11",
    "pydantic-settings>=2.7",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8",
    "pytest-asyncio>=0.24",
    "pytest-cov>=6",
    "httpx>=0.28",
    "ruff>=1.0",
    "mypy>=1.18",
]

# --- poetry-managed project (existing codebases) ---
# [tool.poetry]
# name = "my-project"
# version = "0.1.0"
# description = "My FastAPI project"
# authors = ["Your Name <you@example.com>"]
#
# [tool.poetry.dependencies]
# python = "^3.14"
# fastapi = {version = "^0.120", extras = ["standard"]}
# pydantic = "^2.11"
# pydantic-settings = "^2.7"
#
# [tool.poetry.group.dev.dependencies]
# pytest = "^8"
# pytest-asyncio = "^0.24"
# pytest-cov = "^6"
# httpx = "^0.28"
# ruff = "^1.0"
# mypy = "^1.18"

[tool.ruff]
line-length = 100
target-version = "py314"

[tool.mypy]
python_version = "3.14"
strict = true

[tool.pytest.ini_options]
asyncio_mode = "auto"  # all async tests run without @pytest.mark.asyncio decorator
testpaths = ["tests"]

[build-system]
requires = ["hatchling"]   # uv default; use "poetry-core" for poetry projects
build-backend = "hatchling.build"
```

**Q69: How do you create a virtual environment manually?**
A: With `uv`, virtual environments are managed automatically — you rarely need to think about them. With `poetry`, same applies. Manual `python -m venv` is available but not recommended in 2026.

```bash
# --- Using uv (recommended) ---
uv sync           # creates .venv and installs all deps automatically
uv run python main.py  # runs inside .venv without activation

# --- Using poetry (existing codebases) ---
poetry install   # creates .venv automatically
poetry shell     # activate venv in current shell

# --- Manual (not recommended — for reference only) ---
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

**Q70: What's the difference between the lockfile and `pyproject.toml`?**
A: `pyproject.toml` specifies version ranges (`">=0.120"`). The lockfile (`uv.lock` for uv projects, `poetry.lock` for poetry projects) has exact pinned versions of all dependencies and sub-dependencies — like `package.json` vs `package-lock.json`. Always commit the lockfile to source control for reproducible builds.

**Q71: How do you debug Python in VS Code?**
A: Use the built-in debugger. Create `.vscode/launch.json`. For FastAPI, use `fastapi dev` as the run target.

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI (fastapi dev)",
      "type": "debugpy",
      "request": "launch",
      "module": "fastapi",
      "args": ["dev", "main.py"],
      "jinja": true,
      "justMyCode": false
    },
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Pytest",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

**Q72: What's `pytest` and how do you use it?**
A: Python testing framework. Like Jest but with fixtures instead of `beforeEach`/`afterEach` hooks.

```python
# tests/test_main.py
from pydantic import BaseModel

class User(BaseModel):
    """User class docstring."""
    name: str
    age: int

def test_user_creation() -> None:
    """test_user_creation function docstring."""
    user = User(name="Alice", age=30)
    assert user.name == "Alice"
    assert user.age == 30
```

```bash
# --- Using uv (recommended) ---
uv run pytest --cov=. --cov-report=term-missing --cov-fail-under=80

# --- Using poetry (existing codebases) ---
poetry run pytest --cov=. --cov-report=term-missing --cov-fail-under=80
```

**Q73: How do you manage environment variables?**
A: Use `pydantic-settings` and `BaseSettings`. No need for a separate `python-dotenv` package — `pydantic-settings` reads `.env` files natively.

```python
# config.py
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Settings class docstring."""
    database_url: str
    secret_key: str
    debug: bool = False

    # dict shorthand — not inner class Config (that is Pydantic v1 legacy)
    model_config = {"env_file": ".env"}


@lru_cache
def get_settings() -> Settings:
    """get_settings function docstring."""
    return Settings()
```

**Q74: What's the Python equivalent of ESLint/Prettier?**
A: `ruff` combines linting + formatting. Historically: `pylint` (lint), `black` (format), `isort` (import sort) — all replaced by `ruff` in 2024–2026.

**Q75: How do you handle git hooks for Python?**
A: Use the `pre-commit` framework to run linters before commits.

```bash
# --- Using uv (recommended) ---
uv add --dev pre-commit

# --- Using poetry (existing codebases) ---
poetry add --group dev pre-commit
```

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v1.0.0 # pin to current stable
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.18.0 # pin to current stable
    hooks:
      - id: mypy
```

```bash
# --- Using uv ---
uv run pre-commit install
uv run pre-commit run --all-files

# --- Using poetry ---
poetry run pre-commit install
poetry run pre-commit run --all-files
```

---

### 🎯 Working Code Artefact 5: Complete Python Project Setup Script

```bash
#!/bin/bash
# setup-python-project.sh
# Complete Python project setup for TypeScript engineers — 2026 edition
# Uses uv (recommended) — see comments for poetry equivalent

set -e

PROJECT_NAME="fastapi-demo"

echo "🚀 Setting up Python project: $PROJECT_NAME"

# 1. Install uv (if not installed)
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

# 2. Install Python 3.14 and pin it for this project
echo "🐍 Installing Python 3.14..."
uv python install 3.14
uv python pin 3.14   # writes .python-version

# 3. Create project
echo "📁 Creating project structure..."
uv init $PROJECT_NAME
cd $PROJECT_NAME

# 4. Add core dependencies — fastapi[standard] bundles uvicorn + fastapi-cli
echo "📦 Adding dependencies..."
uv add "fastapi[standard]" pydantic pydantic-settings

# 5. Add dev dependencies
uv add --dev \
    ruff \
    mypy \
    pytest \
    pytest-asyncio \
    pytest-cov \
    httpx \
    pre-commit

# --- Poetry equivalent (for existing codebases) ---
# poetry new $PROJECT_NAME && cd $PROJECT_NAME
# poetry add "fastapi[standard]" pydantic pydantic-settings
# poetry add --group dev ruff mypy pytest pytest-asyncio pytest-cov httpx pre-commit

# 6. Create directory structure
mkdir -p ${PROJECT_NAME}/api
mkdir -p ${PROJECT_NAME}/models
mkdir -p ${PROJECT_NAME}/services
mkdir -p tests/api

# 7. Create main.py
cat > ${PROJECT_NAME}/main.py << 'EOF'
"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    yield
    print("Shutting down")


app = FastAPI(title="FastAPI Demo", version="0.1.0", lifespan=lifespan)


@app.get("/health", response_model=HealthResponse, include_in_schema=False)
async def health() -> HealthResponse:
    return HealthResponse(status="healthy", version="0.1.0")
EOF

# 8. Create test file using AsyncClient pattern (consistent with Days 2+)
cat > tests/test_main.py << 'EOF'
"""Tests for main application."""

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi_demo.main import app


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
EOF

# 9. Write pyproject.toml tool config
cat >> pyproject.toml << 'EOF'

[tool.ruff]
line-length = 100
target-version = "py314"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.mypy]
python_version = "3.14"
strict = true
warn_return_any = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = "-v --cov=fastapi_demo --cov-report=term-missing"
EOF

# 10. Create .env.example
cat > .env.example << 'EOF'
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
SECRET_KEY=your-secret-key-here-minimum-32-chars
DEBUG=false
EOF

# 11. Makefile with uv — fastapi dev for development, fastapi run for production
cat > Makefile << 'EOF'
.PHONY: install lint format test dev prod clean

install:
	uv sync

lint:
	uv run ruff check .
	uv run mypy .

format:
	uv run ruff format .
	uv run ruff check --fix .

test:
	uv run pytest --cov-fail-under=80

dev:
	uv run fastapi dev fastapi_demo/main.py    # hot reload — development only

prod:
	uv run fastapi run fastapi_demo/main.py    # no reload — production

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov
EOF

# 12. Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
.coverage
htmlcov/
.env
.env.local
.DS_Store
EOF

# 13. VS Code settings
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.analysis.typeCheckingMode": "strict",
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "ruff.lint.enable": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false
}
EOF

# 14. VS Code launch config — fastapi dev
cat > .vscode/launch.json << 'EOF'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI (fastapi dev)",
      "type": "debugpy",
      "request": "launch",
      "module": "fastapi",
      "args": ["dev", "fastapi_demo/main.py"],
      "jinja": true,
      "justMyCode": false
    },
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Pytest",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal"
    }
  ]
}
EOF

# 15. pre-commit config with 2026 versions
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v1.0.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.18.0
    hooks:
      - id: mypy
        additional_dependencies: [pydantic, pydantic-settings]
EOF

# 16. Install dependencies and hooks
echo "📦 Installing dependencies..."
uv sync

echo "🔗 Installing pre-commit hooks..."
uv run pre-commit install

echo "✨ Formatting code..."
uv run ruff format .

echo "🧪 Running tests..."
uv run pytest

echo ""
echo "✅ Project setup complete!"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  make dev     # fastapi dev — hot reload, Swagger UI at http://localhost:8000/docs"
echo "  make test    # run tests with coverage"
echo "  make lint    # ruff + mypy"
```

### ✅ Key Concepts

- **`uv` manages everything in new projects**: Python version, venv, and deps — like nvm + npm combined, written in Rust
- **`poetry` is the established alternative**: Still prevalent in existing codebases and interviews — senior engineers know both
- **`ruff` replaces multiple tools**: Linting + formatting in one Rust binary (100× faster than the tools it replaces)
- **`fastapi dev main.py` is the 2026 dev command** (hot reload) — `fastapi run main.py` for production; `fastapi[standard]` bundles `fastapi-cli` + `uvicorn[standard]` + `httpx`
- **`asyncio_mode = "auto"` in pyproject.toml** — all `async def` test functions run without `@pytest.mark.asyncio` decorator
- **VS Code integration**: Auto-format on save, inline type errors from mypy

### ⚠️ Common Pitfalls

- Not activating virtual environment when using poetry (use `poetry shell` or `poetry run`); with uv, `uv run` handles this automatically
- Installing packages globally instead of in project (always use `uv add` or `poetry add`)
- Forgetting to run `uv sync` / `poetry install` after cloning (no `node_modules` equivalent — `.venv` is gitignored)
- Using `uvicorn main:app --reload` when `fastapi dev main.py` is available — both work but `fastapi dev` is the 2026 standard
- Using `fastapi dev` in production — use `fastapi run` for production deployments (no hot reload, production-grade)
- Not configuring VS Code to use the project's Python interpreter — causes missing import errors

---

## 💡 Practice Exercises

### Exercise 1: Type System Mastery

Create a typed Python module that models a simple e-commerce system:

- `Product` model with name, price, SKU — use PEP 695 `type` aliases for `ProductId = int` and `SKU = str`
- `Order` model with items list, total, status enum
- `User` model with optional shipping address
- Function that calculates order total with full type hints
- Must pass `mypy --strict` with no errors

### Exercise 2: Dataclasses vs Pydantic

Implement the same `User` model using both dataclasses and Pydantic, then write a comparison function that:

- Shows serialisation differences (`.model_dump()` vs `asdict()`)
- Demonstrates runtime validation in Pydantic vs manual `__post_init__` validation
- Benchmarks performance difference using `timeit`
- Shows `SecretStr` behaviour on the Pydantic version

### Exercise 3: Async Concurrency

Build an async script that:

- Fetches data from 10 mock API endpoints concurrently using `asyncio.gather()`
- Implements retry logic with exponential backoff
- Has a 5-second timeout per request using `asyncio.wait_for()`
- Rate-limits to max 3 concurrent requests using `asyncio.Semaphore`
- Uses an async context manager for resource cleanup

### Exercise 4: Complete Project Setup

Using the setup script as reference:

- Create a new FastAPI project from scratch with `uv init` (or `poetry new` if working in an existing poetry codebase)
- Add a `/users` endpoint with CRUD operations, Pydantic request/response schemas, and `SecretStr` on the password field
- Write async tests using `AsyncClient` + `ASGITransport` with 80%+ coverage
- Configure `ruff`, `mypy`, `pre-commit`, and `asyncio_mode = "auto"`
- Ensure `make lint && make test` both pass

---

## 🎤 UK Interview Prep Questions

### Junior to Mid-Level (£50k–£70k)

**Q76: Explain the difference between `list` and `tuple` in Python.**
A: Lists are mutable (can change), tuples are immutable (fixed). Tuples are faster and hashable (can be dict keys). Use lists for collections that change, tuples for fixed data.

**Q77: What's the difference between `==` and `is` in Python?**
A: `==` checks value equality, `is` checks identity (same object in memory). Use `==` for value comparison, `is` for `None` checks and singletons.

**Q78: How do you handle exceptions in Python?**
A: Use `try`/`except`/`finally`. Be specific with exception types. Never use a bare `except:` in production — it swallows `KeyboardInterrupt` and `SystemExit`.

```python
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Value error: {e}")
    raise
except Exception as e:
    logger.exception("Unexpected error")
    raise
finally:
    cleanup()
```

**Q79: What are decorators in Python?**
A: Functions that wrap other functions to modify behaviour. Common in frameworks (FastAPI routes, pytest fixtures, `@field_validator` in Pydantic).

```python
import time
from typing import Callable, Any

def timing_decorator(func: Callable) -> Callable:
    """timing_decorator function docstring."""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """wrapper method docstring."""
        # This still works perfectly
        # result = add(3, 4)        # any number of arguments -> touple *args = (3, 4)
        # result = add(a=10, b=20)  # any number of key word argument -> dict **kwargs = {'a': 10, 'b': 20}
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - start:.3f}s")
        return result
    return wrapper

@timing_decorator
def slow_function() -> None:
    """slow_function function docstring."""
    time.sleep(1)
```

**Q80: Explain list comprehensions.**
A: Concise way to create lists. More Pythonic than for-loops for simple transformations.

```python
# Traditional loop
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension (preferred)
squares = [x ** 2 for x in range(10)]

# With condition
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
```

### Mid to Senior Level (£70k–£90k)

**Q81: How does Python's GIL affect concurrency?**
A: The Global Interpreter Lock (GIL) means only one thread executes Python bytecode at a time. Use `asyncio` for I/O-bound tasks (network, DB — the GIL is released during I/O waits), `multiprocessing` for CPU-bound work. The GIL does not affect async/await performance — the event loop is single-threaded by design. Python 3.14 supports free-threaded builds (PEP 703), removing the GIL for CPU-bound parallel workloads. Free-threaded mode is still maturing across the ecosystem; multiprocessing remains the safe default for CPU-bound work until library support is universal.

**Q82: Explain context managers and their use cases.**
A: Objects that implement `__enter__` and `__exit__` (or `__aenter__`/`__aexit__` for async). Ensure resource cleanup (files, DB connections, locks). Use the `with` statement.

```python
from contextlib import contextmanager

@contextmanager
def timer():
    """timer function docstring."""
    start = time.perf_counter()
    yield
    print(f"Took {time.perf_counter() - start:.3f}s")

with timer():
    expensive_operation()
```

**Q83: What's the difference between `@staticmethod` and `@classmethod`?**
A: `@staticmethod` receives neither class nor instance — it is a plain function namespaced to the class. `@classmethod` receives the class as first arg (`cls`) — use it for alternate constructors.

```python
class User:
    """User class docstring."""
    def __init__(self, name: str) -> None:
        """__init__ method docstring."""
        self.name = name

    @classmethod
    def from_dict(cls, data: dict) -> "User":  # alternate constructor
        """from_dict method docstring."""
        return cls(data["name"])

    @staticmethod
    def validate_name(name: str) -> bool:  # no class/instance needed
        """validate_name method docstring."""
        return len(name) > 0
```

**Q84: How do you optimise slow Python code?**
A: Profile first (`cProfile`, `line_profiler`). Use generators for large datasets, NumPy for numeric operations, `functools.lru_cache` for memoisation, `asyncio` for I/O-bound work, `multiprocessing` for CPU-bound work.

**Q85: Explain Python's method resolution order (MRO).**
A: Order Python searches for methods in inheritance. Uses C3 linearisation algorithm. Check with `ClassName.__mro__`. Matters in multiple inheritance — relevant when building the SQLAlchemy `AsyncAttrs + MappedAsDataclass + DeclarativeBase` combined base class in Day 3.

### Senior Level (£90k–£130k)

**Q86: How would you design a type-safe API client in Python?**
A: Use Pydantic models for requests/responses, PEP 695 generics for a reusable client, `httpx.AsyncClient` for async calls, retry decorators for transient failures, and structured logging.

```python
from pydantic import BaseModel
import httpx

class ApiClient[T: BaseModel]:
    """ApiClient class docstring."""
    def __init__(self, base_url: str) -> None:
        """__init__ method docstring."""
        self._client = httpx.AsyncClient(base_url=base_url)

    async def get(self, path: str, model: type[T]) -> T:
        response = await self._client.get(path)
        response.raise_for_status()
        return model.model_validate(response.json())
```

**Q87: How do you handle database migrations in production?**
A: Use Alembic with FastAPI (introduced Day 3). Generate migrations from model changes with `alembic revision --autogenerate`, review the SQL, test on staging, run with `alembic upgrade head`. Use zero-downtime strategies for breaking changes (add column → backfill → remove old column in three separate deploys). Always commit migration files to source control.

**Q88: Explain your approach to async exception handling in FastAPI.**
A: Custom exception handlers for domain errors, middleware for unexpected errors, structured logging with `structlog`, return RFC 7807 problem details for consistency.

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class DomainError(Exception):
    """DomainError class docstring."""
    def __init__(self, message: str, status_code: int = 400) -> None:
        """__init__ method docstring."""
        self.message = message
        self.status_code = status_code

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message, "type": "domain_error"},
    )
```

**Q89: How do you structure a large FastAPI application?**
A: Domain-driven structure: `api/` (routes — no business logic), `services/` (business logic), `models/` (SQLAlchemy ORM), `schemas/` (Pydantic request/response), `repositories/` (DB queries), `core/` (config, dependencies, security). Use `APIRouter` for modularity, `Annotated` + PEP 695 `type` aliases for dependency injection, `lifespan` for startup/shutdown.

**Q90: Explain your testing strategy for async Python code.**
A: `pytest-asyncio` with `asyncio_mode = "auto"` for async tests; `httpx.AsyncClient` with `ASGITransport` for FastAPI integration tests (no network socket); `dependency_overrides` for mocking DB and auth; `factory-boy` for test data generation; `unittest.mock.patch` for external calls; coverage minimum 80% enforced in CI.

---

---

## 🧪 Advanced / Senior-Level: Typed DataFrames (Optional)

> This section is not required for beginners. It targets senior engineers working in data-adjacent Python roles.

As Python's typing ecosystem has matured, typed DataFrames have become a senior-level expectation in roles that blend backend engineering with data pipelines. Libraries like **`pandera`** allow you to define DataFrame schemas with full type annotations and runtime validation — similar to how Pydantic validates dictionaries at API boundaries.

```python
import pandera as pa
from pandera.typing import DataFrame, Series

class UserSchema(pa.DataFrameModel):
    """UserSchema class docstring."""
    user_id: Series[int] = pa.Field(ge=1)
    name: Series[str]
    age: Series[int] = pa.Field(ge=0, le=150)
    email: Series[str]

    class Config:
        """Config class docstring."""
        coerce = True

@pa.check_types
def process_users(df: DataFrame[UserSchema]) -> DataFrame[UserSchema]:
    """process_users function docstring."""
    return df[df["age"] >= 18]
```

**When this matters:** data pipeline roles, ML feature engineering, ETL services. **At FastAPI-only roles:** knowledge is a differentiator, not a prerequisite. Mention `pandera` if the role includes data processing responsibilities.

---

## 📚 Additional Resources

### Official Documentation

- **Python typing module**: https://docs.python.org/3/library/typing.html
- **PEP 695 — Type Aliases**: https://peps.python.org/pep-0695/
- **PEP 593 — `Annotated`**: https://peps.python.org/pep-0593/
- **PEP 703 — Free-threading**: https://peps.python.org/pep-0703/
- **Pydantic v2 docs**: https://docs.pydantic.dev/latest/
- **pydantic-settings**: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- **asyncio documentation**: https://docs.python.org/3/library/asyncio.html
- **uv documentation**: https://docs.astral.sh/uv/
- **Poetry documentation**: https://python-poetry.org/docs/
- **Ruff documentation**: https://docs.astral.sh/ruff/

### Mental Model Mapping (TS → Python)

| TypeScript                    | Python                            | Notes                                              |
| ----------------------------- | --------------------------------- | -------------------------------------------------- |
| `interface`                   | `Protocol` or `TypedDict`         | Structural vs nominal typing                       |
| `type X = ...`                | `type X = ...` (PEP 695)          | Native type alias — Python 3.12+, standard in 3.14 |
| `string \| number`            | `str \| int`                      | Union types                                        |
| `string \| null \| undefined` | `str \| None`                     | Optional types                                     |
| `Promise<T>`                  | `Coroutine[Any, Any, T]`          | Async return types                                 |
| `async/await`                 | `async/await`                     | Nearly identical syntax                            |
| `T extends BaseType`          | `T: BaseType` (PEP 695 bound)     | Generic constraints                                |
| `npm` / `pnpm`                | `uv` (modern) / `poetry` (legacy) | Package managers                                   |
| `ESLint` + `Prettier`         | `ruff`                            | Linting + formatting                               |
| `tsc`                         | `mypy`                            | Static type checking                               |
| `package.json`                | `pyproject.toml`                  | Project config + tool config                       |
| `node_modules`                | `.venv`                           | Dependencies location                              |
| `Jest`                        | `pytest`                          | Testing frameworks                                 |
| `Zod`                         | `Pydantic v2`                     | Runtime validation                                 |
| `class-validator`             | `@field_validator`                | Field-level validation                             |
| `string` (sensitive fields)   | `SecretStr`                       | Prevents accidental logging                        |

---

## ✅ Today's Deliverable Checklist

By the end of today, you should have:

- [ ] Installed `uv` and used `uv python install 3.14` to pin Python 3.14
- [ ] Created a new Python project with `uv init` (or `poetry new` if working in an existing poetry codebase)
- [ ] Added `ruff`, `mypy`, `pytest`, `pytest-asyncio`, and `httpx` to dev dependencies
- [ ] Configured `pyproject.toml` with correct 2026 version pins and `asyncio_mode = "auto"`
- [ ] Configured VS Code with Ruff extension, format on save, and `fastapi dev` debug config
- [ ] Written a typed Python module with type hints that passes `mypy --strict`
- [ ] Used PEP 695 `type` aliases and generic functions (`def fn[T]`) in at least one module
- [ ] Created at least one dataclass and one Pydantic model with `SecretStr` on a sensitive field
- [ ] Used `model_config = {"env_file": ".env"}` (not legacy `class Config:`)
- [ ] Written and run an async function using `asyncio.gather()` for concurrent execution
- [ ] Run `ruff format .` and `ruff check .` with zero errors
- [ ] Run `mypy .` with zero errors
- [ ] Understood the difference between `fastapi dev` (development, hot reload) and `fastapi run` (production)
- [ ] Committed your first Python project to GitHub

---

**Next Sprint Day:** Tue 21 Apr — FastAPI Production Setup: `APIRouter`, dependency injection with `Annotated` + PEP 695 `type` aliases, Pydantic request/response schemas, middleware, CORS, background tasks. Build a `/users` CRUD API.

---

_This learning material is part of the 2026 Python · Azure · AI Engineering Roadmap targeting UK senior roles (£90k–£130k / £550–£750/day). Python 3.14 · uv · FastAPI · Pydantic v2 · ruff · mypy._
