// Handling speech recognition when the speaker icon is clicked
document.getElementById('speaker').addEventListener('click', () => {
    const recognition = new webkitSpeechRecognition() || new SpeechRecognition();
    recognition.lang = 'en-US';

    recognition.onresult = function(event) {
        const speechResult = event.results[0][0].transcript;
        // You can handle the speech result here, for example, send it to a backend API
        console.log('Speech result:', speechResult);
    };

    recognition.start();
});
