"""Call the Watson NLP emotion service and normalize its response."""

from typing import Any, Dict, Optional

import requests

EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTION_NAMES = ("anger", "disgust", "fear", "joy", "sadness")


def emotion_detector(text_to_analyze: str) -> Optional[Dict[str, Any]]:
    """Return five emotion scores and the dominant emotion for the text.

    Returns None when the service rejects the input or a request/response
    error prevents a trustworthy result from being produced.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return None

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
        return None

    if response.status_code == 400:
        return None
    if response.status_code != 200:
        return None

    try:
        body = response.json()
        # The Watson workflow response wraps the emotion scores in an
        # emotionPredictions list. Use a defensive lookup to avoid indexing
        # malformed responses without validation.
        predictions = body.get("emotionPredictions", [])
        if not predictions:
            return None
        emotion_block = predictions[0].get("emotion", {})
        scores = {name: float(emotion_block[name]) for name in EMOTION_NAMES}
    except (ValueError, TypeError, KeyError, AttributeError):
        return None

    result: Dict[str, Any] = dict(scores)
    result["dominant_emotion"] = max(scores, key=scores.get)
    return result
