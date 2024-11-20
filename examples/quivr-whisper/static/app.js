const recordBtn = document.getElementById('record-btn');
const audioVisualizer = document.getElementById('audio-visualizer');
const audioPlayback = document.getElementById('audio-playback');
const canvasCtx = audioVisualizer.getContext('2d');

let isRecording = false;
let mediaRecorder;
let audioChunks = [];
let audioContext;
let analyser;
let dataArray;
let bufferLength;
let lastAudioLevel = 0;
let silenceTimer;

recordBtn.addEventListener('click', toggleRecording);

function toggleRecording() {
    if (!isRecording) {
        recordBtn.classList.add('hidden');
        audioVisualizer.classList.remove('hidden');
        startRecording();
    } else {
        audioVisualizer.classList.add('hidden');
        stopRecording();
    }
}

function drawWaveform() {
    if (!analyser) return;

    requestAnimationFrame(drawWaveform);

    analyser.getByteTimeDomainData(dataArray);

    canvasCtx.fillStyle = 'rgb(255, 255, 255)';
    canvasCtx.fillRect(0, 0, audioVisualizer.width, audioVisualizer.height);

    canvasCtx.lineWidth = 2;
    canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

    canvasCtx.beginPath();

    let sliceWidth = audioVisualizer.width * 1.0 / bufferLength;
    let x = 0;

    let sum = 0;

    for (let i = 0; i < bufferLength; i++) {
        let v = dataArray[i] / 128.0;
        let y = v * audioVisualizer.height / 2;

        sum += v;

        if (i === 0) {
            canvasCtx.moveTo(x, y);
        } else {
            canvasCtx.lineTo(x, y);
        }

        x += sliceWidth;
    }

    canvasCtx.lineTo(audioVisualizer.width, audioVisualizer.height / 2);
    canvasCtx.stroke();

    let currentAudioLevel = sum / bufferLength;

    if (isRecording && Math.abs(currentAudioLevel - lastAudioLevel) < 0.01) {
        if (!silenceTimer) {
            silenceTimer = setTimeout(stopRecording, 1000);
        }
    } else {
        clearTimeout(silenceTimer);
        silenceTimer = null;
    }

    lastAudioLevel = currentAudioLevel;
}

async function startRecording() {
    audioChunks = [];
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = event => {
        audioChunks.push(event.data);
    };
    mediaRecorder.start();
    isRecording = true;

    audioContext = new (window.AudioContext || window.webkitAudioContext)();
    analyser = audioContext.createAnalyser();
    const source = audioContext.createMediaStreamSource(stream);

    source.connect(analyser);
    analyser.fftSize = 2048;
    bufferLength = analyser.frequencyBinCount;
    dataArray = new Uint8Array(bufferLength);

    drawWaveform();
}

function stopRecording() {
    mediaRecorder.stop();
    mediaRecorder.onstop = async () => {
        // The mediaRecorder has stopped; now we can process the chunks
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio_data', audioBlob);

        // Now we're sending the audio to the server and waiting for a response
        try {
            const response = await fetch('/transcribe', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            // Once we have the response, we can source the playback element and play it
            audioPlayback.src = 'data:audio/wav;base64,' + data.audio_base64;
            audioPlayback.classList.remove('hidden');
            audioVisualizer.classList.add('hidden'); // hide the visualizer while playing back the response
            setupAIResponseVisualization();
            audioPlayback.onloadedmetadata = () => {
                // When metadata is loaded, start playback
                audioPlayback.play();
                visualizeAIResponse();
            };

            // We only reset the UI after the audio has finished playing
            // audioPlayback.onended = () => {
            //     resetUI();
            // };
        } catch (error) {
            console.error('Error during fetch/transcription:', error);
            resetUI();
        } finally {
            if (analyser) {
                analyser.disconnect();
                analyser = null;
            }
            isRecording = false;
        }
    };
}
function resetUI() {
    document.getElementById('record-btn').classList.remove('hidden');
    document.getElementById('audio-visualizer').classList.add('hidden');
    document.getElementById('audio-playback').classList.add('hidden');
    // Reset any other UI elements as necessary
}

function setupAIResponseVisualization() {
    try {
        // Create a new audio context for playback if it doesn't exist
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        // Resume the audio context in case it's in a suspended state
        audioContext.resume().then(() => {
            analyser = audioContext.createAnalyser();
            const source = audioContext.createMediaElementSource(audioPlayback);
            source.connect(analyser);
            analyser.connect(audioContext.destination);
            analyser.fftSize = 2048;
            bufferLength = analyser.frequencyBinCount;
            dataArray = new Uint8Array(bufferLength);
        });
    } catch (error) {
        console.error('Error setting up AI response visualization:', error);
    }
}

function visualizeAIResponse() {
    const draw = () => {
        requestAnimationFrame(draw);

        analyser.getByteTimeDomainData(dataArray);

        canvasCtx.fillStyle = 'rgb(255, 255, 255)';
        canvasCtx.fillRect(0, 0, audioVisualizer.width, audioVisualizer.height);

        canvasCtx.lineWidth = 2;
        canvasCtx.strokeStyle = 'rgb(0, 0, 0)';

        canvasCtx.beginPath();

        let sliceWidth = audioVisualizer.width * 1.0 / bufferLength;
        let x = 0;

        for (let i = 0; i < bufferLength; i++) {
            let v = dataArray[i] / 128.0;
            let y = v * audioVisualizer.height / 2;

            if (i === 0) {
                canvasCtx.moveTo(x, y);
            } else {
                canvasCtx.lineTo(x, y);
            }

            x += sliceWidth;
        }

        canvasCtx.lineTo(audioVisualizer.width, audioVisualizer.height / 2);
        canvasCtx.stroke();
    };

    draw();
}