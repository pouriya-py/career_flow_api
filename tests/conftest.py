# tests/conftest.py
import sys
import os
from pathlib import Path

# اضافه کردن مسیر ریشه پروژه به sys.path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# تنظیمات اضافی برای pytest
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Fixture برای دسترسی به TestClient در همه تست‌ها"""
    return TestClient(app)