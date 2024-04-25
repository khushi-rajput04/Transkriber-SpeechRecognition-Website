from flask import Flask, render_template, request, redirect
import speech_recognition as sr
from jinja2 import Template

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    status_message = ""
    if request.method == "POST":
        if "transcribe_file" in request.form:
            return redirect("/transcribe_file")
        elif "transcribe_microphone" in request.form:
            return redirect("/transcribe_microphone")
    return render_template('index.html', transcript=transcript, status_message=status_message)

@app.route("/transcribe_file", methods=["GET", "POST"])
def transcribe_file(): # Input as audio file
    transcript = ""
    status_message = ""
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file.filename != "":
                recognizer = sr.Recognizer()
                audio_file = sr.AudioFile(file)
                with audio_file as source:
                    audio_data = recognizer.record(source)
                transcript = recognizer.recognize_google(audio_data, key=None)
    return render_template('index.html', transcript=transcript, status_message=status_message)

@app.route("/transcribe_microphone", methods=["GET", "POST"])
def transcribe_microphone(): # Input from microphone
    transcript = ""
    status_message = ""
    if request.method == "POST":
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        with microphone as source:
            # status_message = "Say something..."
            recognizer.adjust_for_ambient_noise(source)
            audio_data = recognizer.listen(source, timeout=5)
            status_message = "Audio Captured"
        try:
            transcript = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            transcript = "Could not understand audio"
        except sr.RequestError as e:
            transcript = "Error: {0}".format(e)
    return render_template('index.html', transcript=transcript, status_message=status_message)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
