// DOM Elements
const recordBtn = document.getElementById("record-btn");
const fileInput = document.getElementById("fileInput");
const fileInputContainer = document.querySelector(".custom-file-input");
const fileName = document.getElementById("fileName");

const audioVisualizer = document.getElementById("audio-visualizer");
const audioPlayback = document.getElementById("audio-playback");
const canvasCtx = audioVisualizer.getContext("2d");

window.addEventListener("load", () => {
  audioVisualizer.width = window.innerWidth;
  audioVisualizer.height = window.innerHeight;
});

window.addEventListener("resize", (e) => {
  audioVisualizer.width = window.innerWidth;
  audioVisualizer.height = window.innerHeight;
});

fileInput.addEventListener("change", () => {
  fileName.textContent =
    fileInput.files.length > 0 ? fileInput.files[0].name : "No file chosen";
  fileName.classList.toggle("file-selected", fileInput.files.length > 0);
});

// Configuration
const SILENCE_THRESHOLD = 128; // Adjusted for byte data (128 is middle)
const SILENCE_DURATION = 1500;
const FFT_SIZE = 2048;

// State
const state = {
  isRecording: false,
  isVisualizing: false,
  chunks: [],
  silenceTimer: null,
  lastAudioLevel: 0,
};

// Audio Analysis
class AudioAnalyzer {
  constructor() {
    this.reset();
  }

  reset() {
    this.analyser = null;
    this.dataArray = null;
    this.bufferLength = null;
    this.source = null;
    this.cleanup();
  }

  setup(source, audioContext) {
    this.cleanup();

    this.analyser = this._createAnalyser(audioContext);
    source.connect(this.analyser);

    this._initializeBuffer();
    return this.analyser;
  }

  setupForPlayback(audioElement, audioContext, connectToDestination = true) {
    // Reuse existing MediaElementSourceNode if it already exists for this audio element
    if (!this.source || this.source.mediaElement !== audioElement) {
      this.cleanup(); // Ensure any previous connections are cleaned up
      this.source = audioContext.createMediaElementSource(audioElement);
    }

    this.analyser = this._createAnalyser(audioContext);

    this.source.connect(this.analyser);

    if (connectToDestination) {
      this.analyser.connect(audioContext.destination);
    }

    this._initializeBuffer();
    return this.analyser;
  }

  cleanup() {
    if (this.source) {
      this._safeDisconnect(this.source);
    }
    if (this.analyser) {
      this._safeDisconnect(this.analyser);
    }
  }

  _createAnalyser(audioContext) {
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = FFT_SIZE;
    return analyser;
  }

  _initializeBuffer() {
    this.bufferLength = this.analyser.frequencyBinCount;
    this.dataArray = new Uint8Array(this.bufferLength);
  }

  _safeDisconnect(node) {
    if (node) {
      try {
        node.disconnect();
      } catch {
        // Ignore disconnect errors
      }
    }
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
    if (!currentAnalyser || this.analyzer.dataArray === null) return;

    requestAnimationFrame(() => this.draw(currentAnalyser, onSilence));

    // Use getByteTimeDomainData instead of getFloatTimeDomainData
    currentAnalyser.getByteTimeDomainData(this.analyzer.dataArray);

    // Clear canvas
    this.ctx.fillStyle = "#252525";
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    if (!state.isVisualizing) return;

    this.ctx.lineWidth = 2;
    this.ctx.strokeStyle = "#6142d4";
    this.ctx.beginPath();

    const sliceWidth = (this.canvas.width * 1) / this.analyzer.bufferLength;
    let x = 0;
    let sum = 0;

    // Draw waveform
    for (let i = 0; i < this.analyzer.bufferLength; i++) {
      // Scale byte data (0-255) to canvas height
      const v = this.analyzer.dataArray[i] / 128.0; // normalize to 0-2
      const y = (v - 1) * (this.canvas.height / 2) + this.canvas.height / 2;

      sum += Math.abs(v - 1); // Calculate distance from center (128)

      if (i === 0) {
        this.ctx.moveTo(x, y);
      } else {
        this.ctx.lineTo(x, y);
      }

      x += sliceWidth;
    }

    this.ctx.lineTo(this.canvas.width, this.canvas.height / 2);
    this.ctx.stroke();

    // Check for silence during recording with adjusted thresholds for byte data
    if (state.isRecording) {
      const averageAmplitude = sum / this.analyzer.bufferLength;
      if (averageAmplitude < 0.1) {
        // Adjusted threshold for normalized data
        // Reset silence timer if we detect sound
        if (averageAmplitude > 0.05) {
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
    this.audioContext = null;
  }

  async initialize() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.setupRecordingEvents();
      if (!this.audioContext)
        this.audioContext = new (window.AudioContext ||
          window.webkitAudioContext)();
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
    state.isVisualizing = true;
    state.chunks = [];
    state.isRecording = true;
    this.mediaRecorder.start();

    const source = this.audioContext.createMediaStreamSource(
      this.mediaRecorder.stream
    );

    const analyser = this.audioAnalyzer.setup(source, this.audioContext);
    audioVisualizer.classList.remove("hidden");

    this.visualizer.draw(analyser, () => {
      if (!state.silenceTimer) {
        state.silenceTimer = setTimeout(
          () => this.stopRecording(),
          SILENCE_DURATION
        );
      }
    });

    recordBtn.dataset.recording = true;
    recordBtn.classList.add("processing");
  }

  stopRecording() {
    if (state.isRecording) {
      state.isVisualizing = false;
      state.isRecording = false;
      this.mediaRecorder.stop();
      clearTimeout(state.silenceTimer);
      state.silenceTimer = null;
      recordBtn.dataset.recording = false;
    }
  }

  async handleRecordingStop() {
    console.log("Processing recording...");
    recordBtn.dataset.pending = true;
    recordBtn.disabled = true;

    const audioBlob = new Blob(state.chunks, { type: "audio/wav" });
    if (!fileInput.files.length) {
      recordBtn.dataset.pending = false;
      recordBtn.disabled = false;
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

    audioPlayback.onloadedmetadata = () => {
      const analyser = this.audioAnalyzer.setupForPlayback(
        audioPlayback,
        this.audioContext
      );
      audioVisualizer.classList.remove("hidden");

      this.visualizer.draw(analyser, () => {});
      audioPlayback.play();
      state.isVisualizing = true;
    };

    audioPlayback.onended = () => {
      this.audioAnalyzer.cleanup();
      recordBtn.dataset.pending = false;
      recordBtn.disabled = false;
      state.isVisualizing = false;
    };
  }
}

const uploadFile = async (e) => {
  uploadBtn.innerText = "Uploading File...";
  e.preventDefault();
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file.");
    return;
  }
  const formData = new FormData();
  formData.append("file", file);
  try {
    await fetch("/upload", {
      method: "POST",
      body: formData,
    });
    recordBtn.classList.remove("hidden");
    fileInputContainer.classList.add("hidden");
  } catch (error) {
    recordBtn.classList.add("hidden");
    fileInputContainer.classList.remove("hidden");
    console.error("Error uploading file:", error);
    uploadBtn.innerText = "Upload Failed. Try again";
  }
};

const uploadBtn = document.getElementById("upload-btn");
uploadBtn.addEventListener("click", uploadFile);

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
