import speech_recognition as sr

def getSpeech(language):
    r = sr.Recognizer()
    mic = sr.Microphone()
    try:
        with mic as mic_source:
            r.adjust_for_ambient_noise(mic_source, duration=0.1)
            
            print("Listening now")
            audio = r.listen(mic_source)

            MyText = r.recognize_google(audio, language=language)
            MyText = MyText.lower()

            return MyText
    
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    
    except sr.UnknownValueError:
        print("unknown error occured")

def getSpeechThreaded(callback):
    r = sr.Recognizer()
    mic = sr.Microphone()
    # r.adjust_for_ambient_noise(mic, duration=0.2)
    
    print("Listening now")
    stop = r.listen_in_background(mic, callback)
    print("Listening in background")
    
    return stop