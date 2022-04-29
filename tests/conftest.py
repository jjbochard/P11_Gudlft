import pytest

import server


# @pytest.fixture
# def client():
#     app = Flask(__name__)
#     app.secret_key = "something_special"
#     with app.test_client() as client:
#         yield client
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
        "competitions": [
            {
                "name": "Spring Festival",
                "date": "2020-03-27 10:00:00",
                "numberOfPlaces": "25",
            },
        ]
    }
