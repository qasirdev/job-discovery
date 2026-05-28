import os

# Set dummy environment variables required by pydantic Settings 
# before any module is imported during test collection.
os.environ["DATABASE_URL"] = "postgresql://test_user:test_password@localhost:5432/test_db"
os.environ["OPENAI_API_KEY"] = "sk-mock-key-for-testing"
os.environ["REDIS_URL"] = "redis://localhost:6379"
