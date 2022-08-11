from locust import HttpUser, between, task


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def show_club(self):
        self.client.get("/clubs")

    @task
    def login(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def wrong_login(self):
        self.client.post("/showSummary", {"email": "john@smplylift.co"})

    @task
    def index(self):
        self.client.get("/")

    @task
    def book(self):
        self.client.get("/book/Fall Classic/Simply Lift")

    @task
    def purchase(self):
        self.client.post(
            "/purchasePlaces",
            {"competition": "Fall Classic", "club": "Simply Lift", "places": "1"},
        )

    @task
    def logout(self):
        self.client.get("/logout")
