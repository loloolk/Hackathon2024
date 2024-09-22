let liveText = '';
let summaryText = '';
let currentLanguage = 'en';
let ttsEnabled = false;
let keywords = [];
let ttsOriginal = false;
let ttsTranslated = false;
let recordAudio = false;

fetch('http://127.0.0.1:5000/changeSettings/InputLanguage', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ model_type: "en" }),
});
fetch('http://127.0.0.1:5000/changeSettings/OutputLanguage', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ model_type: "en" }),
});
fetch('http://127.0.0.1:5000/changeSettings/VoiceModel', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ model_type: "alloy" }),
});
fetch('http://127.0.0.1:5000/clearTexts');

function toggleSettings() {
    const settingsPopup = document.getElementById('settings');
    settingsPopup.style.display = settingsPopup.style.display === 'block' ? 'none' : 'block';
}

function changeVoice() {
    const voice = document.getElementById('voiceSelect').value;
    console.log(`Voice changed to: ${voice}`);
    fetch('http://127.0.0.1:5000/changeSettings/VoiceModel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ model_type: voice }),
    });
}

function changeInputLanguage() {
    currentLanguage = document.getElementById('languageInputSelect').value;
    console.log(`Input Language changed to: ${currentLanguage}`);
    fetch('http://127.0.0.1:5000/changeSettings/InputLanguage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input_language: currentLanguage }),
    });
}

function changeOutputLanguage() {
    currentLanguage = document.getElementById('languageOutputSelect').value;
    console.log(`Output Language changed to: ${currentLanguage}`);
    fetch('http://127.0.0.1:5000/changeSettings/OutputLanguage', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ output_language: currentLanguage }),
    });
}

function changeFont() {
    const font = document.getElementById('fontSelect').value;
    document.body.style.fontFamily = font;
}

function changeFontSize() {
    const fontSize = document.getElementById('fontSizeSelect').value;
    document.body.style.fontSize = fontSize === 'small' ? '14px' :
                                   fontSize === 'medium' ? '16px' :
                                   fontSize === 'large' ? '18px' :
                                   fontSize === 'x-large' ? '20px' : '24px';
}

function speakUntranslatedText() {
    fetch('http://127.0.0.1:5000/speakUntranslatedText');
}

function speakTranslatedText() {
    fetch('http://127.0.0.1:5000/speakTranslatedText');
}

function translateText() {
    fetch('http://127.0.0.1:5000/translateText')
    .then(response => response.json())
        .then(data => {
            const translateTextElement = document.getElementById('translationText');
            translateTextElement.textContent = data.translated_text;
            if (translateTextElement.scrollHeight > translateTextElement.clientHeight) {
                translateTextElement.scrollTop = translateTextElement.scrollHeight;
            }
        });
}
function clearTexts() {
    fetch('http://127.0.0.1:5000/clearTexts');
}

function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
}


function toggleRecording() {
    recordAudio = !recordAudio;
    console.log(recordAudio);
    const recordButton = document.getElementById('recordButton');
    if (recordAudio) {
        recordButton.textContent = '⏹️ Stop';
        recordButton.classList.add('recording');
        startRecording();
    }
    else {
        recordButton.textContent = '🎙️ Record';
        recordButton.classList.remove('recording');
        stopRecording();
    }
}
function startRecording() {
    fetch('http://127.0.0.1:5000/startSpeechThreaded')
        .then(() => {
            console.log('Recording started');
        });
}
function stopRecording() {
    fetch('http://127.0.0.1:5000/stopSpeechThreaded')
        .then(() => {
            console.log('Recording stopped');
        });
}
function updateLive() {
    if (recordAudio == true) {
        fetch('http://127.0.0.1:5000/getText')
        .then(response => response.json())
        .then(data => {
            const liveTextElement = document.getElementById('liveText');
            liveTextElement.textContent = data.prev_recorded_text;
            if (liveTextElement.scrollHeight > liveTextElement.clientHeight) {
                liveTextElement.scrollTop = liveTextElement.scrollHeight;
            }
        });
    }
}


setInterval(updateLive, 1000);

// Initialize dark mode
document.body.classList.add('dark-mode');

