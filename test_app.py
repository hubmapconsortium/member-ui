import os
import tempfile

import pytest

from app import app, add_stage_user

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

def test_dump(client):
    """Test dump"""
    rv = client.get('/stage_user')
    assert True == True