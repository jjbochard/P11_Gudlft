from server import (
    MAX_PLACES_ALLOWED_PER_COMPETITION,
    club_has_enough_points,
    loadFile,
    placesIntoPoints,
    pointsIntoPlaces,
    updateClubs,
    updateCompetitions,
)


class TestUnit:
    def test_load_file(self):
        test_clubs = loadFile("tests/test_clubs.json")
        expected_clubs = [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]

        assert test_clubs == expected_clubs

    def test_update_clubs(self, tearDownClubs):

        list_club_before_update = loadFile("tests/test_update_clubs.json")
        points_before_update = list_club_before_update[0]["points"]
        point_used = 1
        assert points_before_update == "13"

        update_list_club_by_using_one_points = [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "12"}
        ]
        updateClubs(
            update_list_club_by_using_one_points, "tests/test_update_clubs.json"
        )
        test_update_clubs = loadFile("tests/test_update_clubs.json")
        expected_value = str(int(points_before_update) - point_used)
        assert test_update_clubs[0]["points"] == expected_value

    def test_update_competitions(self, tearDownCompetitions):

        list_competition_before_update = loadFile("tests/test_update_competitions.json")
        places_before_update = list_competition_before_update[0]["places"]
        place_purchased = 1
        assert places_before_update == "25"

        update_list_competition_by_purchasing_one_place = [
            {"name": "Spring Festival", "date": "2023-03-27 10:00:00", "places": "24"}
        ]
        updateCompetitions(
            update_list_competition_by_purchasing_one_place,
            "tests/test_update_competitions.json",
        )
        test_update_competitions = loadFile("tests/test_update_competitions.json")
        expected_value = str(int(places_before_update) - place_purchased)
        assert test_update_competitions[0]["places"] == expected_value

    def test_club_has_enough_points(self):
        assert club_has_enough_points(3, 9) is True
        assert club_has_enough_points(3, 3) is True
        assert club_has_enough_points(3, 2) is False

    def test_convert_points_into_places(self):
        assert pointsIntoPlaces(3) == 1
        assert pointsIntoPlaces(7) == 2

    def test_convert_places_into_points(self):
        assert placesIntoPoints(3) == 9


class TestClass:
    def test_book_exceed_number_of_points(self, client, test_club, test_competition):
        points_before_purchase = test_club["points"]
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": test_competition["name"],
                "club": test_club["name"],
                "places": 2,
            },
        )
        assert response.status_code == 200
        assert test_club["points"] == points_before_purchase

    def test_book_exceed_number_of_points_per_competititon(
        self, client, test_club, test_competition
    ):
        points_before_purchase = test_club["points"]
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": test_competition["name"],
                "club": test_club["name"],
                "places": MAX_PLACES_ALLOWED_PER_COMPETITION + 1,
            },
        )

        assert response.status_code == 200
        assert test_club["points"] == points_before_purchase

    def test_book_places_in_past_competition(
        self, client, test_club, test_past_competition
    ):
        points_before_purchase = test_club["points"]
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": test_past_competition["name"],
                "club": test_club["name"],
                "places": 1,
            },
        )
        assert response.status_code == 200
        assert "You cannot book places in past competition" in response.data.decode()
        assert test_club["points"] == points_before_purchase
