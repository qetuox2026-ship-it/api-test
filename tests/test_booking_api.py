import pytest


pytestmark = pytest.mark.regression

@pytest.mark.smoke
def test_get_booking_list(booking_client):
    response = booking_client.get_booking_list()

    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) > 0
    assert "bookingid" in response_data[0]

@pytest.mark.smoke
def test_create_booking(created_booking):
    response_data = created_booking["create_response_data"]
    expected_data = created_booking["booking_data"]

    assert isinstance(response_data["bookingid"], int)
    assert response_data["booking"] == expected_data

@pytest.mark.smoke
def test_get_created_booking(booking_client, created_booking):
    booking_id = created_booking["booking_id"]
    expected_data = created_booking["booking_data"]

    response = booking_client.get_booking(booking_id)

    assert response.status_code == 200
    assert response.json() == expected_data


def test_update_booking(
    booking_client,
    created_booking,
    auth_token,
    updated_booking_data
):
    booking_id = created_booking["booking_id"]



    update_response = booking_client.update_booking(
        booking_id=booking_id,
        booking_data=updated_booking_data,
        token=auth_token
    )

    assert update_response.status_code == 200
    assert update_response.json() == updated_booking_data

    get_response = booking_client.get_booking(booking_id)

    assert get_response.status_code == 200
    assert get_response.json() == updated_booking_data


def test_delete_booking(booking_client, created_booking, auth_token):
    booking_id = created_booking["booking_id"]

    delete_response = booking_client.delete_booking(
        booking_id=booking_id,
        token=auth_token
    )

    assert delete_response.status_code == 201

    get_response = booking_client.get_booking(booking_id)

    assert get_response.status_code == 404