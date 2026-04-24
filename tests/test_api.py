import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivitiesAPI:
    """Test suite for the Activities API endpoints"""

    def test_get_activities(self):
        """Test GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

        # Check that each activity has the required fields
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_specific_activity(self):
        """Test that specific activities are returned correctly"""
        response = client.get("/activities")
        data = response.json()

        # Check Chess Club exists and has correct structure
        assert "Chess Club" in data
        chess_club = data["Chess Club"]
        assert chess_club["max_participants"] == 12
        assert len(chess_club["participants"]) >= 0

    def test_signup_successful(self):
        """Test successful signup for an activity"""
        # Use a test email that shouldn't exist
        test_email = "test.student@mergington.edu"
        activity_name = "Chess Club"

        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert test_email in data["message"]
        assert activity_name in data["message"]

        # Verify the participant was added
        get_response = client.get("/activities")
        activities = get_response.json()
        assert test_email in activities[activity_name]["participants"]

    def test_signup_duplicate_email(self):
        """Test that signing up with the same email twice fails"""
        test_email = "duplicate.test@mergington.edu"
        activity_name = "Programming Class"

        # First signup should succeed
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        assert response1.status_code == 200

        # Second signup should fail
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        assert response2.status_code == 400
        data = response2.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_nonexistent_activity(self):
        """Test signup for non-existent activity fails"""
        test_email = "test@mergington.edu"
        nonexistent_activity = "NonExistent Activity"

        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": test_email}
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_successful(self):
        """Test successful unregister from an activity"""
        test_email = "unregister.test@mergington.edu"
        activity_name = "Gym Class"

        # First sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        assert signup_response.status_code == 200

        # Then unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": test_email}
        )

        assert unregister_response.status_code == 200
        data = unregister_response.json()
        assert "message" in data
        assert test_email in data["message"]
        assert activity_name in data["message"]

        # Verify the participant was removed
        get_response = client.get("/activities")
        activities = get_response.json()
        assert test_email not in activities[activity_name]["participants"]

    def test_unregister_not_signed_up(self):
        """Test unregistering someone who isn't signed up fails"""
        test_email = "not.signed.up@mergington.edu"
        activity_name = "Tennis Club"

        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": test_email}
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not registered" in data["detail"]

    def test_unregister_nonexistent_activity(self):
        """Test unregister from non-existent activity fails"""
        test_email = "test@mergington.edu"
        nonexistent_activity = "NonExistent Activity"

        response = client.delete(
            f"/activities/{nonexistent_activity}/unregister",
            params={"email": test_email}
        )

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_root_redirect(self):
        """Test root endpoint redirects to static index"""
        response = client.get("/")
        assert response.status_code == 200
        # FastAPI's RedirectResponse should redirect to the static file
        # In test client, it follows redirects by default
        assert "text/html" in response.headers.get("content-type", "")