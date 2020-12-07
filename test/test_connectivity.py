import requests
class TestConnectivity:
    def test_connection_to_webhook(self):
        assert requests.post("http://localhost:5000/bot").status_code ==  200