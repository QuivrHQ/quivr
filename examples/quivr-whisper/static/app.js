const recordBtn = document.getElementById("record-btn");
const fileInput = document.getElementById("fileInput");

const audioVisualizer = document.getElementById("audio-visualizer");
const audioPlayback = document.getElementById("audio-playback");
const canvasCtx = audioVisualizer.getContext("2d");

let analyser;
let bufferLength;
let dataArray;
let lastAudioLevel = 0;
let silenceTimer;
let silenceThreshold = 0.05; // Adjustable silence threshold
let silenceDuration = 1500; // Milliseconds of silence before stopping

let isRecording = false;

if (navigator.mediaDevices) {
  const constraints = { audio: true };
  let chunks = [];

  navigator.mediaDevices
    .getUserMedia(constraints)
    .then((stream) => {
      const mediaRecorder = new MediaRecorder(stream);

      const drawWaveform = () => {
        if (!analyser) return;

        requestAnimationFrame(drawWaveform);

        analyser.getByteTimeDomainData(dataArray);

        canvasCtx.fillStyle = "rgb(255, 255, 255)";
        canvasCtx.fillRect(0, 0, audioVisualizer.width, audioVisualizer.height);

        canvasCtx.lineWidth = 2;
        canvasCtx.strokeStyle = "rgb(0, 0, 0)";

        canvasCtx.beginPath();

        let sliceWidth = (audioVisualizer.width * 1.0) / bufferLength;
        let x = 0;

        let sum = 0;
        let maxAmplitude = 0;

        for (let i = 0; i < bufferLength; i++) {
          let v = dataArray[i] / 128.0 - 1; // Normalize to [-1, 1]
          let y = (v * audioVisualizer.height) / 2;

          // Calculate absolute amplitude
          sum += Math.abs(v);
          maxAmplitude = Math.max(maxAmplitude, Math.abs(v));

          if (i === 0) {
            canvasCtx.moveTo(x, y + audioVisualizer.height / 2);
          } else {
            canvasCtx.lineTo(x, y + audioVisualizer.height / 2);
          }

          x += sliceWidth;
        }

        canvasCtx.lineTo(audioVisualizer.width, audioVisualizer.height / 2);
        canvasCtx.stroke();

        // More robust silence detection
        let averageAmplitude = sum / bufferLength;

        if (
          isRecording &&
          averageAmplitude < silenceThreshold &&
          maxAmplitude < silenceThreshold * 2
        ) {
          if (!silenceTimer) {
            silenceTimer = setTimeout(stopRecording, silenceDuration);
          }
        } else {
          clearTimeout(silenceTimer);
          silenceTimer = null;
        }

        lastAudioLevel = averageAmplitude;
      };

      const startRecording = () => {
        chunks = []; // Reset chunks at start of recording
        mediaRecorder.start();
        isRecording = true;
        console.log(mediaRecorder.state);
        console.log("recorder started");
        audioVisualizer.classList.remove("hidden");

        const audioContext = new (window.AudioContext ||
          window.webkitAudioContext)();
        analyser = audioContext.createAnalyser();
        const source = audioContext.createMediaStreamSource(stream);

        source.connect(analyser);
        analyser.fftSize = 2048;
        bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);

        drawWaveform();
      };

      const stopRecording = () => {
        if (isRecording) {
          mediaRecorder.stop();
          isRecording = false;
          console.log(mediaRecorder.state);
          console.log("recorder stopped due to silence");
          audioVisualizer.classList.add("hidden");
        }
      };

      recordBtn.onclick = () => {
        if (mediaRecorder.state === "inactive") {
          startRecording();
        } else if (mediaRecorder.state === "recording") {
          stopRecording();
        }
      };

      mediaRecorder.onstop = async (e) => {
        console.log("STOPP");

        // The mediaRecorder has stopped; now we can process the chunks
        const audioBlob = new Blob(chunks, { type: "audio/wav" });
        const formData = new FormData();

        formData.append("audio_data", audioBlob);

        // Append the file to the FormData object
        if (fileInput.files.length > 0) {
          formData.append("file", fileInput.files[0]);
        } else {
          alert("Please select a file.");
          return;
        }

        // Now we're sending the audio to the server and waiting for a response
        try {
          const response = await fetch("/ask", {
            method: "POST",
            body: formData,
          });
          const data = await response.json();
          console.log(data);

          // Once we have the response, we can source the playback element and play it
          audioPlayback.src = "data:audio/wav;base64," + data.audio_base64;
          audioPlayback.classList.remove("hidden");
          audioVisualizer.classList.add("hidden"); // hide the visualizer while playing back the response
          audioPlayback.onloadedmetadata = () => {
            // When metadata is loaded, start playback
            audioPlayback.play();
          };
        } catch (error) {
          console.error("Error during fetch/transcription:", error);
        } finally {
          if (analyser) {
            analyser.disconnect();
            analyser = null;
          }
        }
      };

      mediaRecorder.ondataavailable = (e) => {
        chunks.push(e.data);
      };
    })
    .catch((err) => {
      console.error(`The following error occurred: ${err}`);
    });
}
