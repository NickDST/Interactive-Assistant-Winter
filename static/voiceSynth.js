// Init SpeechSynth API
const synth = window.speechSynthesis;


//Browser identifier
// Firefox 1.0+
var isFirefox = typeof InstallTrigger !== 'undefined';

// Chrome 1+
var isChrome = !!window.chrome && !!window.chrome.webstore;


// Init voices array
let voices = [];

const getVoices = () => {
    voices = synth.getVoices();
    
};

//Fix for duplication, run code depending on the browser
if (isFirefox) {
    getVoices();
}

getVoices();

if (synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = getVoices;
}

console.log(voices);


// Speak
function winterSpeak(vm, textInput){

    // Check if speaking
    if (synth.speaking) {
      console.error('Already speaking...');
      return;
    }
    if (textInput !== '') {
      // Get speak text
      const speakText = new SpeechSynthesisUtterance(textInput);
  
      // Speak end
      speakText.onend = e => {
        console.log('Done speaking...');
      };
  
      // Speak error
      speakText.onerror = e => {
        console.error('Something went wrong');
      };
  
    //   // Selected voice
    //   const selectedVoice = voiceSelect.selectedOptions[0].getAttribute(
    //     'data-name'
    //   );
  
    const selectedVoice = "Google UK English Female";

      // Loop through voices
      voices.forEach(voice => {
        if (voice.name === selectedVoice) {
          speakText.voice = voice;
        }
      });
  
      // Set pitch and rate
      speakText.rate = 1;
      speakText.pitch = 1;
      // Speak
      synth.speak(speakText);
    }
}