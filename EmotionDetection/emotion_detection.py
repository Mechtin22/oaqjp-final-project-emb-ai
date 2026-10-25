"""Call the Watson NLP emotion service and normalize its response."""

from typing import Any, Dict

import requests

EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result() -> Dict[str, Any]:
    """Return the rubric-required result when no prediction is available."""
    return {
        "anger": None,
        "disgust": None,
        "fear": None,
        "joy": None,
        "sadness": None,
        "dominant_emotion": None,
    }


def emotion_detector(text_to_analyze: str) -> Dict[str, Any]:
    """Return emotion scores and the dominant emotion for the supplied text.

    All expected result keys are returned, with None values when the request
    is blank, rejected by the service, or cannot be processed safely.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    headers = {"grpc-metadata-mm-model-id": MODEL_ID}
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            EMOTION_URL,
            json=payload,
            headers=headers,
            timeout=20,
        )
    except requests.RequestException:
        return _empty_result()

    if response.status_code == 400:
        return _empty_result()
    if response.status_code != 200:
        return _empty_result()

    try:
        body = response.json()
        predictions = body.get("emotionPredictions", [])
        if not predictions:
            return _empty_result()
        emotion_block = predictions[0].get("emotion", {})
        scores = {name: float(emotion_block[name]) for name in EMOTION_NAMES}
    except (ValueError, TypeError, KeyError, AttributeError):
        return _empty_result()

    result: Dict[str, Any] = dict(scores)
    result["dominant_emotion"] = max(scores, key=scores.get)
    return result
