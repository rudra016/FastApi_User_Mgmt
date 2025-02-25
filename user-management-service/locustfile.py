from locust import HttpUser, task, between
import random

class AuthUser(HttpUser):
    wait_time = between(1, 2)  # Simulates a real user waiting between requests
    token = None  # Store token for authenticated requests
    users = []  # Store signed-up users for login

    @task(1)
    def signup(self):
        """Simulates user signup and stores credentials"""
        email = f"testuser{random.randint(1, 10000)}@example.com"
        payload = {
            "email": email,
            "password": "TestPassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post("/auth/signup", json=payload)
        if response.status_code == 201:
            self.users.append(email)  # Store for login
            print(f"Signup successful: {email}")

    @task(2)
    def login(self):
        """Simulates user login using stored credentials"""
        if not self.users:
            return  # Avoid login attempt if no users are available

        email = random.choice(self.users)  # Pick a signed-up user
        payload = {
            "email": email,
            "password": "TestPassword123"
        }
        response = self.client.post("/auth/login", json=payload)
        if response.status_code == 200:
            self.token = response.json()["token"]
            print(f"Login successful: {email}")

    @task(2)
    def protected_route(self):
        """Access protected route if logged in"""
        if self.token:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.client.get("/protected", headers=headers)
            if response.status_code == 200:
                print("Protected route accessed")

    @task(1)
    def logout(self):
        """Logs out user"""
        if self.token:
            response = self.client.post("/auth/logout", params={"user_id": 1})
            if response.status_code == 200:
                print("User logged out")
                self.token = None