from flask import Flask, render_template, request, jsonify, send_from_directory
import pyttsx3
import os
import shutil

app = Flask(__name__)

AUDIO_DIR = os.path.join(os.getcwd(), 'audio')

if os.path.exists(AUDIO_DIR):
    shutil.rmtree(AUDIO_DIR)
os.makedirs(AUDIO_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data.get('text', '')
    voice_choice = data.get('voice', 'female')  
    speed = data.get('speed', 150)  

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    engine = pyttsx3.init()

    engine.setProperty('rate', int(speed))

    voices = engine.getProperty('voices')
    voice_found = False
    for voice in voices:
        if voice_choice == 'female' and "Zira" in voice.name:
            engine.setProperty('voice', voice.id)
            voice_found = True
            break
        elif voice_choice == 'male' and "David" in voice.name:
            engine.setProperty('voice', voice.id)
            voice_found = True
            break

    if not voice_found:
        print("Selected voice not found. Using default voice.")

    audio_file_name = f"{hash(text)}.mp3"
    audio_file_path = os.path.join(AUDIO_DIR, audio_file_name)

    engine.save_to_file(text, audio_file_path)
    engine.runAndWait()

    print("Generated audio file path:", audio_file_path)

    return jsonify({'audio_url': f'/audio/{audio_file_name}'})

@app.route('/audio/<filename>')
def send_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
