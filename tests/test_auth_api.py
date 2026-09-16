import pytest


pytestmark = pytest.mark.regression


@pytest.mark.smoke
def test_create_token_success(booking_client):
    response = booking_client.create_token(
        username="admin",
        password="password123"
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "token" in response_data
    assert isinstance(response_data["token"], str)
    assert len(response_data["token"]) > 0


@pytest.mark.parametrize(
    "username, password",
    [
        pytest.param(
            "admin",
            "wrong-password",
            id="wrong-password"
        ),
        pytest.param(
            "wrong-user",
            "password123",
            id="wrong-username"
        ),
        pytest.param(
            "",
            "",
            id="empty-credentials"
        ),
    ]
)
def test_create_token_failed(booking_client, username, password):
    response = booking_client.create_token(
        username=username,
        password=password
    )

    assert response.status_code == 200

    response_data = response.json()

    assert "token" not in response_data
    assert response_data["reason"] == "Bad credentials"