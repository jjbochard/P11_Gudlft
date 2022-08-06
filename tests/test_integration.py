import pytest

import server
from tests.conftest import mock_load_clubs, mock_load_competitions
from utils import MAX_PLACES_ALLOWED_PER_COMPETITION


class TestClass:
    @pytest.fixture(autouse=True)
    def mock_db(self, mocker):
        mocker.patch.object(server, "competitions", mock_load_competitions())
        mocker.patch.object(server, "clubs", mock_load_clubs())
        return mocker

    def test_main_page(self, client):
        response = client.get("/")
        message = "Welcome to the GUDLFT Registration Portal!"

        assert response.status_code == 200
        assert message in response.data.decode()

    def test_logout(self, client):
        response = client.get("/logout")
        message = (
            'You should be redirected automatically to target URL: <a href="/">/</a>'
        )

        assert response.status_code == 302
        assert message in response.data.decode()

    def test_clubs_page(self, client):
        response = client.get("/clubs")
        message = "Clubs Summary"

        assert response.status_code == 200
        assert message in response.data.decode()

    def test_login_with_valid_email(self, client):
        response = client.post(
            "/showSummary",
            data={
                "email": "john@simplylift.co",
            },
        )
        message = "Welcome, john@simplylift.co"

        assert response.status_code == 200
        assert message in response.data.decode()

    def test_login_with_invalid_email(self, client):
        response = client.post(
            "/showSummary",
            data={"email": "test@test.com"},
        )
        message = (
            'You should be redirected automatically to target URL: <a href="/">/</a>'
        )

        assert response.status_code == 302
        assert message in response.data.decode()

    def test_book_places_on_competition(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": 2,
            },
        )
        messages = [
            "Points available: 194",
            "Great-booking complete!",
        ]

        assert response.status_code == 200
        for m in messages:
            assert m in response.data.decode()

    def test_book_exceed_number_of_points(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Not enough club points",
                "places": 2,
            },
        )
        messages = [
            "Your club has not enough points to purchase 2 places",
            "Points available: 2",
        ]

        assert response.status_code == 200
        for m in messages:
            assert m in response.data.decode()

    def test_book_exceed_number_of_points_per_competititon(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": MAX_PLACES_ALLOWED_PER_COMPETITION + 1,
            },
        )
        messages = [
            "You cannot book more than 12 places per competition",
            "Points available: 200",
        ]
        assert response.status_code == 200
        for m in messages:
            assert m in response.data.decode()

    def test_cannot_book_places_in_past_competititon(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Fall Classic",
                "club": "Simply Lift",
                "places": 1,
            },
        )

        assert response.status_code == 200
        messages = [
            "You cannot book places in past competition",
            "Points available: 200",
        ]
        for m in messages:
            assert m in response.data.decode()

    def test_cannot_book_less_than_one_place(self, client):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": 0,
            },
        )
        messages = [
            "You cannot book less than one place",
            "Points available: 200",
        ]

        assert response.status_code == 200
        for m in messages:
            assert m in response.data.decode()

    def test_choose_competition_for_booking_places(self, client):
        club = "Simply Lift"
        competition = "Spring Festival"

        response = client.get(
            f"/book/{competition}/{club}",
        )
        messages = [
            competition,
            "Places availables: 20",
        ]
        assert response.status_code == 200
        for m in messages:
            assert competition in response.data.decode()
