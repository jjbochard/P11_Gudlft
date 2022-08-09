from locust import HttpUser, between, task


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

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
            {"competition": "Fall Classic", "club": "Simply Lift", "places": "0"},
        )

    def on_stop(self):

        self.client.get("/logout")
