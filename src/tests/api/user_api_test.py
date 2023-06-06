from time import sleep


class TestPostCreateUser:
    payload = {
        "username": "testuser",
        "password": "Password12"
    }

    def test_with_valid_data(self, test_app):
        response = test_app.post("/user/create", json=self.payload)
        assert response.status_code == 201
        assert response.json() == {"success": True}

    def test_with_existing_user(self, test_app):
        expected_response_data = {"success": False, "reason": "User already exists"}
        test_app.post("/user/create", json=self.payload)
        response = test_app.post("/user/create", json=self.payload)
        assert response.status_code == 400
        assert response.json() == expected_response_data

    def test_with_invalid_username(self, test_app):
        self.payload["username"] = "us"
        expected_response_data = {"success": False, "reason": "length must be atleast 3 characters"}

        response = test_app.post("/user/create", json=self.payload)
        assert response.status_code == 400
        assert response.json() == expected_response_data

        expected_response_data["reason"] = "length must not exceed 32 characters"
        self.payload["username"] = "abvder" * 6
        response = test_app.post("/user/create", json=self.payload)
        assert response.status_code == 400
        assert response.json() == expected_response_data

    def test_with_invalid_password(self, test_app):
        self.payload["username"] = "us"
        expected_response_data = {"success": False, "reason": "length must be atleast 3 characters"}

        response = test_app.post("/user/create", json=self.payload)
        assert response.status_code == 400
        assert response.json() == expected_response_data


class TestPostVerifyUser:
    payload = {
        "username": "testuser",
        "password": "Password12"
    }

    def test_with_valid_data(self, test_app):
        test_app.post("/user/create", json=self.payload)
        response = test_app.post("/user/verify", json=self.payload)
        assert response.status_code == 200
        assert response.json() == {"success": True}

    def test_with_not_existing_user(self, test_app):
        self.payload["username"] = "not_existing_user"
        response = test_app.post("/user/verify", json=self.payload)
        assert response.status_code == 400
        assert response.json() == {"success": False, "reason": "User doesn't exists, please create your account first"}

    def test_with_incorrect_password(self, test_app):
        self.payload["username"] = "testuser"
        test_app.post("/user/create", json=self.payload)

        self.payload["password"] = "incorrect"
        response = test_app.post("/user/verify", json=self.payload)
        assert response.status_code == 400
        assert response.json() == {"success": False, "reason": "Incorrect password. Please try again."}

    def test_block_for_one_minute(self, test_app):
        self.payload["password"] = "GoodPassword1"
        test_app.post("/user/create", json=self.payload)

        self.payload["password"] = "badPassword"

        for _ in range(5):
            response = test_app.post("/user/verify", json=self.payload)
            assert response.status_code == 400
            assert response.json() == {"success": False, "reason": "Incorrect password. Please try again."}

        response = test_app.post("/user/verify", json=self.payload)
        assert response.status_code == 429
        assert response.json() == {"success": False, "reason": "Too many incorrect attempts. Please wait for 60 seconds before trying again."}

        sleep(60)
        response = test_app.post("/user/verify", json=self.payload)
        assert response.status_code == 400
        assert response.json() == {"success": False, "reason": "Incorrect password. Please try again."}
