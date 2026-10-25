# Emotion Detector — Watson NLP and Flask

A Python web application that uses the course-provided Watson NLP emotion service to analyze text and display scores for **anger, disgust, fear, joy, and sadness**, along with the dominant emotion.

## Features

- Watson NLP emotion prediction.
- A normalized Python result containing five emotion scores and `dominant_emotion`.
- Flask interface and JSON endpoint.
- Blank-input validation, HTTP 400 handling, response validation, and network-error handling.
- Automated unit tests using mocked service responses so tests do not require a live service.

## Requirements

- Python 3.9 or newer
- Internet access for live emotion analysis

## Install and run (Windows / VS Code)

```powershell
python -m pip install -r requirements.txt
python server.py
```

Open http://127.0.0.1:5000 in your browser.

## Run unit tests

```powershell
python -m unittest -v test_emotion_detection.py
```

The tests use mocks for deterministic testing; they do not claim that the external Watson endpoint is currently reachable.

## Static code analysis

```powershell
python -m pylint server.py
```

Review the diagnostics and rerun PyLint after any fixes. Only report a 10.00/10 score when the command actually displays that result.

## Routes

- `GET /` — show the web application.
- `GET /emotionDetector?textToAnalyze=...` — analyze non-empty text and return JSON.
- Blank input returns HTTP 400.
- An upstream or response-processing error returns HTTP 502.

## Project structure

```text
EmotionDetection/
    __init__.py
    emotion_detection.py
server.py
test_emotion_detection.py
requirements.txt
templates/index.html
static/mywebscript.js
```

## Screenshots for the Coursera rubric

Capture real screenshots on your own computer after running the application:

- `6b_deployment_test.png` — running app showing a successful analysis.
- `7c_error_handling_interface.png` — app showing the blank-input validation message.

Do not submit illustrative or fabricated terminal output as evidence. The Watson service endpoint is the training environment's external service and may be unavailable outside that environment.
