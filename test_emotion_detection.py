"""Unit tests for EmotionDetection response handling."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Verify normalized results and service-error handling."""

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_returns_formatted_emotion_scores(self, post):
        response = Mock(status_code=200)
        response.json.return_value = {
            "emotionPredictions": [{
                "emotion": {
                    "anger": 0.01,
                    "disgust": 0.02,
                    "fear": 0.03,
                    "joy": 0.90,
                    "sadness": 0.04,
                }
            }]
        }
        post.return_value = response

        result = emotion_detector("I am happy today")

        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(set(result), {
            "anger", "disgust", "fear", "joy", "sadness", "dominant_emotion"
        })

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_handles_http_400(self, post):
        post.return_value = Mock(status_code=400)
        self.assertIsNone(emotion_detector("invalid request"))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_handles_other_http_errors(self, post):
        post.return_value = Mock(status_code=503)
        self.assertIsNone(emotion_detector("hello"))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_handles_connection_error(self, post):
        post.side_effect = requests.ConnectionError("offline")
        self.assertIsNone(emotion_detector("hello"))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_handles_malformed_response(self, post):
        response = Mock(status_code=200)
        response.json.return_value = {"unexpected": []}
        post.return_value = response
        self.assertIsNone(emotion_detector("hello"))

    def test_blank_text_is_rejected_without_request(self):
        with patch("EmotionDetection.emotion_detection.requests.post") as post:
            self.assertIsNone(emotion_detector("   "))
            post.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
