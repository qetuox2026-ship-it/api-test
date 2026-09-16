import json
import os
from copy import deepcopy
from pathlib import Path

import pytest

from clients.booking_client import BookingClient


PROJECT_ROOT = Path(__file__).parent
CONFIG_FILE = PROJECT_ROOT / "config" / "environments.json"
DATA_FILE = PROJECT_ROOT / "data" / "booking_data.json"
REPORT_DIR = PROJECT_ROOT / "reports"


def load_json(file_path):
    with file_path.open(
        mode="r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="test",
        help="运行环境，例如 test"
    )


@pytest.fixture(scope="session")
def environment_config(request):
    environments = load_json(CONFIG_FILE)
    environment_name = request.config.getoption("--env")

    if environment_name not in environments:
        pytest.fail(
            f"找不到环境配置：{environment_name}"
        )

    return environments[environment_name]


@pytest.fixture(scope="session")
def booking_client(environment_config):
    return BookingClient(
        base_url=environment_config["base_url"],
        timeout=environment_config["timeout"]
    )


@pytest.fixture(scope="session")
def test_data():
    return load_json(DATA_FILE)


@pytest.fixture
def booking_data(test_data):
    return deepcopy(test_data["create_booking"])


@pytest.fixture
def updated_booking_data(test_data):
    return deepcopy(test_data["update_booking"])


@pytest.fixture(scope="session")
def auth_token(booking_client):
    username = os.getenv("BOOKER_USERNAME", "admin")
    password = os.getenv("BOOKER_PASSWORD", "password123")

    response = booking_client.create_token(
        username=username,
        password=password
    )

    assert response.status_code == 200

    response_data = response.json()
    assert "token" in response_data

    return response_data["token"]


@pytest.fixture
def created_booking(booking_client, booking_data, auth_token):
    response = booking_client.create_booking(booking_data)

    assert response.status_code == 200

    response_data = response.json()
    booking_id = response_data["bookingid"]

    yield {
        "booking_id": booking_id,
        "booking_data": booking_data,
        "create_response_data": response_data
    }

    booking_client.delete_booking(
        booking_id=booking_id,
        token=auth_token
    )

def pytest_configure(config):
    REPORT_DIR.mkdir(exist_ok=True)