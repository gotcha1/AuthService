import pytest
from starlette.testclient import TestClient
import os
import sys


tests_dir = os.path.dirname(__file__)
src_dir = os.path.dirname(tests_dir)
sys.path.append(os.path.join(src_dir, "app"))

from app.main import app


@pytest.fixture()
def test_app():
    with TestClient(app) as client:
        yield client
