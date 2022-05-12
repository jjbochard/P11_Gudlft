from server import MAX_PLACES_ALLOWED_PER_COMPETITION, loadFile, updateClubs


class TestUnit:
    def test_load_file(self):
        test_clubs = loadFile("tests/test_clubs.json")
        expected_clubs = [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]

        assert test_clubs == expected_clubs

    def test_update_clubs(self, tearDown):

        list_club_before_update = loadFile("tests/test_update_clubs.json")
        points_before_update = list_club_before_update[0]["points"]
        assert points_before_update == "13"

        update_list_club_by_purchasing_one_place = [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "12"}
        ]
        updateClubs(
            update_list_club_by_purchasing_one_place, "tests/test_update_clubs.json"
        )
        test_update_clubs = loadFile("tests/test_update_clubs.json")
        expected_value = str(int(points_before_update) - 1)
        assert test_update_clubs[0]["points"] == expected_value


class TestClass:
    def test_book_exceed_number_of_points(self, client, test_club, test_competition):
        points_before_purchase = test_club["points"]
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": test_competition["name"],
                "club": test_club["name"],
                "places": int(test_club["points"]) + 1,
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
