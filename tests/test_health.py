import pytest
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

from app import create_app

@pytest.fixture
def client():
    # Create an instance of your app configured for testing
    app = create_app()
    app.config['TESTING'] = True  # Enable testing mode
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    # Test the /health endpoint
    response = client.get('/health')
    assert response.status_code == 200, "Expected status code 200 for /health endpoint"

    # Parse and check the JSON response
    data = response.get_json()
    assert data is not None, "No JSON response from /health"
    assert data.get('status') == 'healthy', "Health status should be 'healthy'"

# Add a simple test to verify pytest is working
def test_simple():
    assert True
