import unittest
from unittest.mock import patch
from kafka_producer import aiven_kafka_producer as akp
import os

class TestAivenKafkaProducer(unittest.TestCase):

    def setUp(self):
        self.producer = akp.AivenKafkaProducer()

    @patch('confluent_kafka.Producer')
    def test_produce_balk_messages(self, mock_kafka_producer):
        mock_producer_instance = mock_kafka_producer.return_value

        messages = [
            {"url": "https://aiven.io", "status_code": 200, "duration": 300},
            {"url": "https://consol.aiven.io", "status_code": 200, "duration": 600}
        ]

        result = self.producer.produce_balk_messages(messages, "url", mock_producer_instance)
        if self.assertTrue(result) == None:
            print("Test Passed! Successfully produced a mock message!")
        if self.assertEqual(mock_producer_instance.produce.call_count, len(messages)) == None:
            print("Test Passed! Both mock messages are produced!")

if __name__ == '__main__':
    unittest.main()