import pytest

import server


@pytest.fixture
def client():
    server.app.config["TESTING"] = True
    yield server.app.test_client()


@pytest.fixture
def test_club():
    return {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13",
    }


@pytest.fixture
def test_competition():
    return {
        "name": "Spring Festival",
        "date": "2020-03-27 10:00:00",
        "numberOfPlaces": "25",
    }


@pytest.fixture
def test_past_competition():
    return {
        "name": "Fall Classic",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "13",
    }


@pytest.fixture
def tearDown():
    yield
    undo_purchase_place = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
    ]
    server.updateClubs(undo_purchase_place, "tests/test_update_clubs.json")
