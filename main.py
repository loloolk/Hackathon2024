from python.stt import getSpeech, getSpeechThreaded
from python.tts import speakText, translateText

print("Welcome to our AI class assistant!")

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
    
    def changeSettings():
        print("Settings:")
        print("1. Change input language")
        print("2. Change output language")
        print("3. Change voice model")
        print("4. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            Vars.changeInputLanguage()
        elif choice == "2":
            Vars.changeOutputLanguage()
        elif choice == "3":
            Vars.changeVoiceModel()
        elif choice == "4":
            main()
        else:
            print("Invalid choice. Please try again.")
            Vars.changeSettings()
    
    def changeInputLanguage():
        print("Select a language:")
        print("Current language: ", Vars.input_language)
        print("Available languages:")
        
        for key, value in Vars.languages.items():
            print(key)
        choice = input("Enter your choice: ")
        
        try:
            Vars.input_language = Vars.languages[choice]
            Vars.changeSettings()
        except KeyError:
            print("Invalid language. Please try again.")
            Vars.changeInputLanguage()
    
    def changeOutputLanguage():
        print("Select a language:")
        print("Current language: ", Vars.output_language)
        print("Available languages:")
        
        for key, value in Vars.languages.items():
            print(key)
        choice = input("Enter your choice: ")
        try:
            Vars.output_language = Vars.languages[choice]
            Vars.changeSettings()
        except KeyError:
            print("Invalid language. Please try again.")
            Vars.changeOutputLanguage()

    def changeVoiceModel():
        print("Select a voice model:")
        print("Current model: ", Vars.model_type)
        print("Available models:")
        print("Default")
        print("Default Male")
        print("Default Female")
        print("Deep Male")
        
        choice = input("Enter your choice: ")
        try:
            Vars.model_type = Vars.models[choice]
            Vars.changeSettings()
        except KeyError:
            print("Invalid model. Please try again.")
            Vars.changeVoiceModel()

def callback(recognizer, audio):
    try:
        Vars.prev_recorded_text += recognizer.recognize_google(audio, language=Vars.input_language)
    except sr.UnknownValueError:
        print("[!] UnknownValueError")
    except sr.RequestError as e:
        print("RequestError: ", e)

def main():
    print("Please select what you would like to do:")
    print("1. Record Speech")
    print("2. Record Speech in Parallel")
    print("3. Stop Recording Speech in Parallel")
    print("4. Translate voice to a different language")
    print("5. Speak the untranslated text")
    print("6. Speak the translated text")
    print("7. Clear recorded text")
    print("8. Settings")
    choice = input("Enter your choice: ")
    if choice == "1":
        Vars.prev_recorded_text = getSpeech(Vars.input_language)
        if Vars.prev_recorded_text == "":
            print("No text detected. Please try again.")
            main()
        else:
            print("Recorded text: ", Vars.prev_recorded_text)
    elif choice == "2":
        if Vars.running:
            print("Already running. Please stop the current recording first.")
            main()
        else:
            Vars.running = True
            Vars.stopper = getSpeechThreaded(callback)
    elif choice == "3":
        if Vars.running:
            Vars.running = False
            Vars.stopper()
        else:
            print("No recording in progress. Please start one first.")
            main()
    elif choice == "4":
        if Vars.prev_recorded_text == "":
            print("No text detected. Please record some text first.")
            main()
        else:
            Vars.translated_text = translateText(Vars.prev_recorded_text, Vars.input_language, Vars.output_language)
            print("Translated text: ", Vars.translated_text)
    elif choice == "5":
        if Vars.prev_recorded_text == "":
            print("No text detected. Please record some text first.")
            main()
        else:
            speakText(Vars.prev_recorded_text, Vars.model_type)
    elif choice == "6":
        if Vars.translated_text == "":
            print("No translated text detected. Please translate some text first.")
            main()
        else:
            speakText(Vars.translated_text, Vars.model_type)
    elif choice == "7":
        Vars.prev_recorded_text = ""
        Vars.translated_text = ""
        print("Cleared recorded text.")
    elif choice == "8":
        Vars.changeSettings()
    else:
        print("Invalid choice. Please try again.")
    
    main()
    
if __name__ == "__main__":
    main()
    