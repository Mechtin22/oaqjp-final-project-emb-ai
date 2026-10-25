"""Unit tests for EmotionDetection response formatting and error handling."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Verify dominant emotion formatting and service-error handling."""

    @staticmethod
    def response_for(dominant):
        """Build a mocked successful response with a known dominant emotion."""
        scores = {
            "anger": 0.01,
            "disgust": 0.02,
            "fear": 0.03,
            "joy": 0.04,
            "sadness": 0.05,
        }
        scores[dominant] = 0.95
        response = Mock(status_code=200)
        response.json.return_value = {
            "emotionPredictions": [{"emotion": scores}]
        }
        return response

    def assert_dominant(self, post, phrase, emotion):
        """Assert that a phrase returns its expected dominant emotion."""
        post.return_value = self.response_for(emotion)
        result = emotion_detector(phrase)
        self.assertEqual(result["dominant_emotion"], emotion)
        self.assertEqual(
            set(result),
            {
                "anger", "disgust", "fear", "joy", "sadness",
                "dominant_emotion",
            },
        )

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_joy(self, post):
        """Check a joy prediction."""
        self.assert_dominant(post, "I am glad this happened", "joy")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_anger(self, post):
        """Check an anger prediction."""
        self.assert_dominant(post, "I am really mad about this", "anger")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_disgust(self, post):
        """Check a disgust prediction."""
        self.assert_dominant(post, "I feel disgusted by this", "disgust")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_sadness(self, post):
        """Check a sadness prediction."""
        self.assert_dominant(post, "I am so sad about this", "sadness")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_fear(self, post):
        """Check a fear prediction."""
        self.assert_dominant(post, "I am afraid of this", "fear")

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_handles_http_400(self, post):
        """Return the required empty result for HTTP 400."""
        post.return_value = Mock(status_code=400)
        result = emotion_detector("invalid request")
        self.assertIsNone(result["dominant_emotion"])
        self.assertTrue(all(
            result[name] is None
            for name in ("anger", "disgust", "fear", "joy", "sadness")
        ))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_handles_other_http_errors(self, post):
        """Return an empty result for non-success status codes."""
        post.return_value = Mock(status_code=503)
        self.assertIsNone(emotion_detector("hello")["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_handles_connection_error(self, post):
        """Return an empty result when the service cannot be reached."""
        post.side_effect = requests.ConnectionError("offline")
        self.assertIsNone(emotion_detector("hello")["dominant_emotion"])

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_handles_malformed_response(self, post):
        """Return an empty result for an unexpected response body."""
        response = Mock(status_code=200)
        response.json.return_value = {"unexpected": []}
        post.return_value = response
        self.assertIsNone(emotion_detector("hello")["dominant_emotion"])

    def test_blank_text_is_rejected_without_request(self):
        """Do not call the service for blank text."""
        with patch("EmotionDetection.emotion_detection.requests.post") as post:
            result = emotion_detector("   ")
            self.assertIsNone(result["dominant_emotion"])
            post.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
