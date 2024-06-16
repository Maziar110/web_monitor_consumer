import unittest
from unittest.mock import patch
from website_health_monitor import web_monitor as wm


test_config_data = {
    "websites": ["https://www.aiven.io"],
    "regex": "\\baiven\\b" 
}

mock_response = {
    "url": "https://www.aiven.io",
    "status_code": 200,
    "total_response_time_ms": 50,
    "is_regex_match": True
}

class TestWebMonitor(unittest.TestCase):

    def setUp(self) -> None:
        self.monitor = wm.WebMonitor(test_config_data)


    @patch('requests.get')
    def test_check_websites_urls(self, mock_get):
        mock_get.return_value.status_code = mock_response["status_code"]
        mock_get.return_value.elapsed.microseconds = mock_response["total_response_time_ms"] * 1000
        mock_get.return_value.text = "Aiven is a versatile platform empowering you with AI-driven \
            workload optimization and control over your data.\
                  Deploy widely adopted technologies \
                    across multiple clouds with just a \
                        few clicks to stream, store, and \
                            serve your data."

        result = self.monitor.check_websites_urls()
        if result is not None and len(result) >= 1:
            print("Test passed! and website was checked successfully!")
            if result[0] == mock_response:
                print("Test passed! The result matches the mock response!")
            else:
                print("Test Failed! The result does not match the mock response!")
                print(f"Expected {mock_response}")
                print(f"Got {result[0]}")
        else:
            print("Test Failed!")

if __name__ == '__main__':
    unittest.main()