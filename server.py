"""Flask web application for Watson NLP emotion detection."""

from flask import Flask, jsonify, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)  # pylint: disable=invalid-name


@app.get("/")
def home():
    """Render the emotion detector user interface."""
    return render_template("index.html")


@app.get("/emotionDetector")
def detect_emotion():
    """Analyze submitted text and return a readable result or validation error."""
    text_to_analyze = request.args.get("textToAnalyze", "").strip()
    if not text_to_analyze:
        return jsonify({
            "error": "Invalid text! Please enter some text to analyze."
        }), 400

    result = emotion_detector(text_to_analyze)
    if result["dominant_emotion"] is None:
        return jsonify({
            "error": (
                "Emotion detection could not process this text. "
                "Please check the input and try again."
            )
        }), 502

    formatted = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, 'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, 'joy': {result['joy']}, "
        f"'sadness': {result['sadness']}. The dominant emotion is "
        f"{result['dominant_emotion']}."
    )
    return jsonify({"result": formatted, "emotions": result}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
