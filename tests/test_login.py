class TestClass:
    def test_login_with_valid_email(self, client, test_club):
        response = client.post(
            "/showSummary",
            data={
                "email": test_club["email"],
            },
        )
        message = f"Welcome, {test_club['email']}"
        assert response.status_code == 200
        assert message in response.data.decode()

    def test_login_with_invalid_email(self, client):
        response = client.post(
            "/showSummary",
            data={"email": "test@test.com"},
        )
        assert response.status_code == 302
