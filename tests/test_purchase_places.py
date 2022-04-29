class TestClass:
    def test_book_exceed_number_of_points(self, client, test_club, test_competition):
        response = client.post(
            "/purchasePlaces",
            data={
                "competition": test_competition["name"],
                "club": test_club["name"],
                "places": int(test_club["points"]) + 1,
            },
        )
        assert response.status_code == 200
        assert (
            f"You cannot use more than your club points ({test_club['points']})"
            in response.data.decode()
        )
        message = f"Points available: {test_club['points']}"
        assert message in response.data.decode()
