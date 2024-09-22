from python.stt import getSpeech
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
    
    prev_recorded_text = ""
    translated_text = ""
    output_language = "en"
    model_type = "alloy"
    
    def changeSettings():
        print("Settings:")
        print("1. Change output language")
        print("2. Change voice model")
        print("3. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            Vars.changeOutputLanguage()
        elif choice == "2":
            Vars.changeVoiceModel()
        elif choice == "3":
            main()
        else:
            print("Invalid choice. Please try again.")
            Vars.changeSettings()
    
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

def main():
    print("Please select what you would like to do:")
    print("1. Record Speech")
    print("2. Translate voice to a different language")
    print("3. Convert text to voice")
    print("4. Settings")
    choice = input("Enter your choice: ")
    if choice == "1":
        Vars.prev_recorded_text = getSpeech()
        if Vars.prev_recorded_text == "":
            print("No text detected. Please try again.")
            main()
        else:
            print("Recorded text: ", Vars.prev_recorded_text)
    elif choice == "2":
        if Vars.prev_recorded_text == "":
            print("No text detected. Please record some text first.")
            main()
        else:
            Vars.translated_text = translateText(Vars.prev_recorded_text, Vars.output_language)
            print("Translated text: ", Vars.translated_text)
    elif choice == "3":
        if Vars.translated_text == "":
            print("No translated text detected. Please translate some text first.")
            main()
        else:
            speakText(Vars.translated_text, Vars.model_type)
    elif choice == "4":
        Vars.changeSettings()
    else:
        print("Invalid choice. Please try again.")
    
    main()
    
if __name__ == "__main__":
    main()
    