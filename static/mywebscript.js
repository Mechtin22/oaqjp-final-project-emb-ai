async function RunSentimentAnalysis() {
    const input = document.getElementById("textToAnalyze");
    const output = document.getElementById("system_response");
    const button = document.getElementById("analyzeButton");
    const textToAnalyze = input.value.trim();

    if (!textToAnalyze) {
        output.textContent = "Invalid text! Please enter some text to analyze.";
        output.classList.add("text-danger");
        return;
    }

    output.classList.remove("text-danger");
    output.textContent = "Analyzing…";
    button.disabled = true;

    try {
        const url = new URL("/emotionDetector", window.location.origin);
        url.searchParams.set("textToAnalyze", textToAnalyze);
        const response = await fetch(url);
        const data = await response.json();

        if (!response.ok) {
            output.textContent = data.error || "The request could not be processed.";
            output.classList.add("text-danger");
            return;
        }

        output.textContent = data.result;
    } catch (error) {
        output.textContent = "Unable to contact the server. Please try again.";
        output.classList.add("text-danger");
    } finally {
        button.disabled = false;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("analyzeButton");
    button.addEventListener("click", RunSentimentAnalysis);
});
