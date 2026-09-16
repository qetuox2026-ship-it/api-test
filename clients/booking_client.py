from time import perf_counter

import requests

from utils.logger import get_logger


logger = get_logger(__name__)


class BookingClient:
    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json"
        })

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        start_time = perf_counter()

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs
            )

            elapsed_time = perf_counter() - start_time

            logger.info(
                "%s %s -> %s, %.2f seconds",
                method,
                url,
                response.status_code,
                elapsed_time
            )

            return response

        except requests.RequestException:
            logger.exception(
                "%s %s request failed",
                method,
                url
            )
            raise

    def get_booking_list(self):
        return self._request("GET", "/booking")

    def get_booking(self, booking_id):
        return self._request(
            "GET",
            f"/booking/{booking_id}"
        )

    def create_booking(self, booking_data):
        return self._request(
            "POST",
            "/booking",
            json=booking_data
        )

    def create_token(self, username, password):
        return self._request(
            "POST",
            "/auth",
            json={
                "username": username,
                "password": password
            }
        )

    def update_booking(self, booking_id, booking_data, token):
        return self._request(
            "PUT",
            f"/booking/{booking_id}",
            json=booking_data,
            cookies={"token": token}
        )

    def delete_booking(self, booking_id, token):
        return self._request(
            "DELETE",
            f"/booking/{booking_id}",
            cookies={"token": token}
        )