from src import app as app_module


def test_get_activities(client):
    # Arrange: none — the fixture ensures clean state

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_prevent_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act — sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert signup succeeded and participant is present
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # Act — attempt duplicate signup
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert duplicate prevented
    assert resp2.status_code == 400


def test_remove_participant(client):
    # Arrange
    activity = "Programming Class"
    email = "temp@mergington.edu"

    # Act — add participant
    add_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert add_resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # Act — remove participant
    del_resp = client.delete(f"/activities/{activity}/participants/{email}")

    # Assert
    assert del_resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]
