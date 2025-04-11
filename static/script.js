let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        mediaRecorder.ondataavailable = event => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav');
            formData.append('lang', document.getElementById('targetLang').value);

            fetch('/process', {
                method: 'POST',
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                document.getElementById('result').innerText = data.translated_text;
            });

            audioChunks = [];
        };
    });
}

function stopRecording() {
    mediaRecorder.stop();
}
