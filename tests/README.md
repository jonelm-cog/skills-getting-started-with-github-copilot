# API Tests

This directory contains comprehensive tests for the Mergington High School Activities API.

## Test Coverage

The test suite covers all API endpoints:

### GET /activities
- Returns all activities with correct structure
- Validates required fields (description, schedule, max_participants, participants)

### POST /activities/{activity_name}/signup
- Successful signup adds participant to activity
- Duplicate signup returns 400 error
- Signup for non-existent activity returns 404 error

### DELETE /activities/{activity_name}/unregister
- Successful unregister removes participant from activity
- Unregistering non-participant returns 404 error
- Unregister from non-existent activity returns 404 error

### GET /
- Root endpoint redirects to static index.html

## Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_api.py::TestActivitiesAPI::test_signup_successful -v
```

## Test Structure

- Uses FastAPI's TestClient for HTTP request testing
- Tests are organized in a class-based structure for better organization
- Each test is independent and doesn't rely on state from other tests
- Covers both success and error scenarios