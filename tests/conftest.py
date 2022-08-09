import pytest

import server
from utils import update_clubs, update_competitions


def mock_load_competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "20",
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
        },
    ]


def mock_load_clubs():
    return [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "200"},
        {
            "name": "Not enough club points",
            "email": "notenoughclubpoints@test.co",
            "points": "2",
        },
    ]


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    yield server.app.test_client()


@pytest.fixture
def tearDownClubs():
    yield
    undo_use_point = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
    ]
    update_clubs(undo_use_point, "tests/test_update_clubs.json")


@pytest.fixture
def tearDownCompetitions():
    yield
    undo_purchase_place = [
        {"name": "Spring Festival", "date": "2023-03-27 10:00:00", "places": "25"}
    ]
    update_competitions(undo_purchase_place, "tests/test_update_competitions.json")
