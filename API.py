import flask
from flask import request, jsonify

from python.stt import getSpeech, getSpeechThreaded
from python.tts import speakText, translateText

app = flask.Flask(__name__)

class Vars:
    languages = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "Mandarin": "zh-CN",
        "Portuguese": "pt",
        "Swahili": "sw",
        "Russian": "ru",
    }
    models = {
        "Default": "alloy",
        "Default Male": "echo",
        "Default Female": "shimmer",
        "Deep Male": "onyx",
    }
    
    # Saved text
    prev_recorded_text = ""
    translated_text = ""
    
    # Input language
    input_language = "en"
    
    # Output language and voice model
    output_language = "en"
    model_type = "alloy"
    
    #Async handling
    running = False
    stopper = None


def callback(recognizer, audio):
    try:
        Vars.prev_recorded_text += recognizer.recognize_google(audio, language=Vars.input_language)
    except speech_recognition.UnknownValueError:
        print("[!] UnknownValueError")
    except speech_recognition.RequestError as e:
        print("RequestError: ", e)


@app.route('/', methods=['GET'])
def index():
    response = {
        "Welcome": "Welcome to our AI class assistant!",
        "Settings": "/changeSettings",
        "Get speech": "/getSpeech",
        "Start speech threaded": "/startSpeechThreaded",
        "Stop speech threaded": "/stopSpeechThreaded",
        "Translate text": "/translateText",
        "Speak untranslated text": "/speakUntranslatedText",
        "Speak translated text": "/speakTranslatedText",
        "Clear texts": "/clearTexts",
    }
    return jsonify(response)

@app.route('/changeSettings', methods=['GET'])
def changeSettings():
    response = {
        "Settings": {
            "Change input language": "changeSettings/InputLanguage",
            "Change output language": "changeSettings/OutputLanguage",
            "Change voice model": "changeSettings/VoiceModel",
            "Back": "/"
        },
        "languages": Vars.languages,
        "models": Vars.models,
        "input_language": Vars.input_language,
    }
    return jsonify(response)
@app.route('/changeSettings/InputLanguage', methods=['POST'])
def changeInputLanguage():
    response = {}
    try:
        data = request.get_json()
        Vars.input_language = data['input_language']
        response["input_language"] = Vars.input_language
    except ValueError:
        response["error"] = "Invalid input language, options are: " + str(Vars.languages.keys())
    return jsonify(response)
@app.route('/changeSettings/OutputLanguage', methods=['POST'])
def changeOutputLanguage():
    response = {}
    try:
        data = request.get_json()
        Vars.output_language = data['output_language']
        response["output_language"] = Vars.output_language
    except ValueError:
        response["error"] = "Invalid output language, options are: " + str(Vars.languages.keys())
    return jsonify(response)

# $.post("127.0.0.1:5000/changeSettings/OutputLanguage", {
    # json_string: JSON.stringify({output_language: "es"})
# }

@app.route('/changeSettings/VoiceModel', methods=['POST'])
def changeVoiceModel():
    response = {}
    try:
        data = request.get_json()
        Vars.model_type = data['model_type']
        response["model_type"] = Vars.model_type
    except ValueError:
        response["error"] = "Invalid model type, options are: " + str(Vars.models.keys())
    return jsonify(response)

@app.route('/getSpeech', methods=['GET'])
def getSpeechF():
    response = {}
    try:
        Vars.prev_recorded_text = getSpeech(Vars.input_language)
        response["recorded_text"] = Vars.prev_recorded_text
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)
@app.route('/startSpeechThreaded', methods=['GET'])
def getSpeechThreadedF():
    response = {}
    try:
        Vars.stopper = getSpeechThreaded(callback)
        response["status"] = "Listening in background"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)
@app.route('/stopSpeechThreaded', methods=['GET'])
def stopSpeechThreaded():
    response = {}
    try:
        Vars.stopper()
        response["status"] = "Stopped listening"
    except Exception as e:
        response["error"] = str(e)
    return jsonify(response)
@app.route('/translateText', methods=['GET'])
def translateTextF():
    response = {}
    try:
        Vars.translated_text = translateText(Vars.prev_recorded_text, Vars.input_language, Vars.output_language)
        response["translated_text"] = Vars.translated_text
    except ValueError:
        response["error"] = "Invalid input"
    return jsonify(response)
@app.route('/speakUntranslatedText', methods=['GET'])
def speakUntranslatedText():
    response = {}
    try:
        speakText(Vars.prev_recorded_text, Vars.model_type)
        response["text"] = Vars.prev_recorded_text
    except ValueError:
        response["error"] = "Invalid input"
    return jsonify(response)
@app.route('/speakTranslatedText', methods=['GET'])
def speakTranslatedText():
    response = {}
    try:
        speakText(Vars.translated_text, Vars.model_type)
        response["translated_text"] = Vars.translated_text
    except ValueError:
        response["error"] = "Invalid input"
    return jsonify(response)
@app.route('/clearTexts', methods=['GET'])
def clearTexts():
    response = {}
    Vars.prev_recorded_text = ""
    Vars.translated_text = ""
    response["prev_recorded_text"] = Vars.prev_recorded_text
    response["translated_text"] = Vars.translated_text
    return jsonify(response)

@app.route('/getText', methods=['GET'])
def getText():
    response = {
        "prev_recorded_text": Vars.prev_recorded_text,
        "translated_text": Vars.translated_text,
    }
    return jsonify(response)
    
app.run(port=5000)