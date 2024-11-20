// DOM Elements
const recordBtn = document.getElementById("record-btn");
const fileInput = document.getElementById("fileInput");
const audioVisualizer = document.getElementById("audio-visualizer");
const audioPlayback = document.getElementById("audio-playback");
const canvasCtx = audioVisualizer.getContext("2d");

// Configuration
const SILENCE_THRESHOLD = 0.01;
const SILENCE_DURATION = 1500;
const FFT_SIZE = 2048;

// State
const state = {
  isRecording: false,
  chunks: [],
  silenceTimer: null,
  lastAudioLevel: 0,
};

// Audio Analysis
class AudioAnalyzer {
  constructor() {
    this.analyser = null;
    this.dataArray = null;
    this.bufferLength = null;
  }

  setup(source, audioContext) {
    this.analyser = audioContext.createAnalyser();
    this.analyser.fftSize = FFT_SIZE;
    source.connect(this.analyser);

    // Change to Float32Array for time domain data
    this.bufferLength = this.analyser.frequencyBinCount;
    this.dataArray = new Float32Array(this.bufferLength);

    return this.analyser;
  }

  setupForPlayback(audioElement, audioContext) {
    const source = audioContext.createMediaElementSource(audioElement);
    const analyser = this.setup(source, audioContext);
    analyser.connect(audioContext.destination);
    return analyser;
  }

  cleanup() {
    if (this.analyser) {
      this.analyser.disconnect();
      this.analyser = null;
    }
    this.dataArray = null;
    this.bufferLength = null;
  }
}

// Visualization
class Visualizer {
  constructor(canvas, analyzer) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.analyzer = analyzer;
  }

  draw(currentAnalyser, onSilence) {
    if (!currentAnalyser) return;

    requestAnimationFrame(() => this.draw(currentAnalyser, onSilence));

    // Use getFloatTimeDomainData instead of getByteTimeDomainData
    currentAnalyser.getFloatTimeDomainData(this.analyzer.dataArray);

    // Clear canvas
    this.ctx.fillStyle = "#252525";
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    this.ctx.lineWidth = 2;
    this.ctx.strokeStyle = "#6142d4";
    this.ctx.beginPath();

    const sliceWidth = (this.canvas.width * 1.0) / this.analyzer.bufferLength;
    let x = 0;
    let sum = 0;
    let maxAmplitude = 0;

    // Draw waveform
    for (let i = 0; i < this.analyzer.bufferLength; i++) {
      // Values are already normalized (-1 to 1), no need to normalize
      const v = this.analyzer.dataArray[i];
      const y = (v * this.canvas.height) / 2 + this.canvas.height / 2;

      sum += Math.abs(v);
      maxAmplitude = Math.max(maxAmplitude, Math.abs(v));

      if (i === 0) {
        this.ctx.moveTo(x, y);
      } else {
        this.ctx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    this.ctx.lineTo(this.canvas.width, this.canvas.height / 2);
    this.ctx.stroke();

    // Check for silence during recording with proper thresholds
    if (state.isRecording) {
      const averageAmplitude = sum / this.analyzer.bufferLength;
      if (averageAmplitude < SILENCE_THRESHOLD) {
        // Reset silence timer if we detect sound
        if (averageAmplitude > SILENCE_THRESHOLD / 2) {
          clearTimeout(state.silenceTimer);
          state.silenceTimer = null;
        } else {
          onSilence();
        }
      }
    }
  }
}

// Recording Handler
class RecordingHandler {
  constructor() {
    this.mediaRecorder = null;
    this.audioAnalyzer = new AudioAnalyzer();
    this.visualizer = new Visualizer(audioVisualizer, this.audioAnalyzer);
  }

  async initialize() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.setupRecordingEvents();
    } catch (err) {
      console.error(`Media device error: ${err}`);
    }
  }

  setupRecordingEvents() {
    this.mediaRecorder.ondataavailable = (e) => {
      state.chunks.push(e.data);
    };

    this.mediaRecorder.onstop = async () => {
      await this.handleRecordingStop();
    };
  }

  startRecording() {
    state.chunks = [];
    state.isRecording = true;
    this.mediaRecorder.start();

    const audioContext = new (window.AudioContext ||
      window.webkitAudioContext)();
    const source = audioContext.createMediaStreamSource(
      this.mediaRecorder.stream
    );

    const analyser = this.audioAnalyzer.setup(source, audioContext);
    audioVisualizer.classList.remove("hidden");

    this.visualizer.draw(analyser, () => {
      if (!state.silenceTimer) {
        state.silenceTimer = setTimeout(
          () => this.stopRecording(),
          SILENCE_DURATION
        );
      }
    });
  }

  stopRecording() {
    if (state.isRecording) {
      state.isRecording = false;
      this.mediaRecorder.stop();
      clearTimeout(state.silenceTimer);
      state.silenceTimer = null;
    }
  }

  async handleRecordingStop() {
    console.log("Processing recording...");

    const audioBlob = new Blob(state.chunks, { type: "audio/wav" });
    if (!fileInput.files.length) {
      alert("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("audio_data", audioBlob);
    formData.append("file", fileInput.files[0]);

    try {
      await this.processRecording(formData);
    } catch (error) {
      console.error("Processing error:", error);
    } finally {
      this.audioAnalyzer.cleanup();
    }
  }

  async processRecording(formData) {
    const response = await fetch("/ask", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    await this.handleResponse(data);
  }

  async handleResponse(data) {
    audioPlayback.src = "data:audio/wav;base64," + data.audio_base64;

    const audioContext = new (window.AudioContext ||
      window.webkitAudioContext)();

    audioPlayback.onloadedmetadata = () => {
      const analyser = this.audioAnalyzer.setupForPlayback(
        audioPlayback,
        audioContext
      );
      audioVisualizer.classList.remove("hidden");

      this.visualizer.draw(analyser, () => {});
      audioPlayback.play();
    };

    audioPlayback.onended = () => {
      this.audioAnalyzer.cleanup();
    };
  }
}

// Main initialization
async function initializeApp() {
  if (!navigator.mediaDevices) {
    console.error("Media devices not supported");
    return;
  }

  const recorder = new RecordingHandler();
  await recorder.initialize();

  recordBtn.onclick = () => {
    if (recorder.mediaRecorder.state === "inactive") {
      recorder.startRecording();
    } else if (recorder.mediaRecorder.state === "recording") {
      recorder.stopRecording();
    }
  };
}

// Start the application
initializeApp();
