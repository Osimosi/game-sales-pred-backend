import json
import pytest
from flask import Flask
from flask_testing import TestCase
from app import app

class TestApp(TestCase):
    def create_app(self):
        return app

    def test_hello(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello World!")

    def test_get_prediction(self):
        sample_request = {
            "CONSOLE": "pc",
            "RATING": "E",
            "CRITICS_POINTS": 1,
            "CATEGORY": "action",
            "YEAR": 2010,
            "PUBLISHER": "Nintendo",
            "USER_POINTS": 1
        }
        response = self.client.post("/get_prediction", data=json.dumps(sample_request), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIsInstance(json.loads(response.data)["result"], float)

    def test_get_prediction_bad_request(self):
        response = self.client.post("/get_prediction", data="not json", content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_not_found(self):
        response = self.client.get("/nonexistent_route")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)["error"], "Not found")

    def test_get_prediction_missing_key(self):
        sample_request = {
        "CONSOLE": "PS4",
        "RATING": "E",
        "CRITICS_POINTS": 7.5,
        "CATEGORY": "Adventure",
        "YEAR": 2018,
        "PUBLISHER": "Sony",
        # "USER_POINTS": 7.8  # Commented out to simulate a missing key
    }
        
        response = self.client.post("/get_prediction", data=json.dumps(sample_request), content_type='application/json')
        self.assertEqual(response.status_code, 400)

def test_get_prediction_invalid_value(self):
    sample_request = {
        "CONSOLE": "PS4",
        "RATING": "E",
        "CRITICS_POINTS": 7.5,
        "CATEGORY": "Adventure",
        "YEAR": 2018,
        "PUBLISHER": "Sony",
        "USER_POINTS": "invalid_value"  # Invalid value for USER_POINTS
    }
    response = self.client.post("/get_prediction", data=json.dumps(sample_request), content_type='application/json')
    self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    pytest.main()
