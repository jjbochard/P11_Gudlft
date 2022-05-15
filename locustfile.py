from locust import HttpUser, between, task


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def hello_world(self):
        self.client.get("/showSummary")

    def on_start(self):
        self.client.post("/", json={"email": "john@simplylift.co"})
