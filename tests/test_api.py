import requests


BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_post():
    response = requests.get(
        f"{BASE_URL}/posts/1",
        timeout=10
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == 1
    assert response_data["userId"] == 1
    assert "title" in response_data