'use client';
import { useState } from 'react';
import axios from 'axios';

export default function ChatPage() {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState([['User', 'Hello!']]);
  const [model, setModel] = useState('gpt-3.5-turbo');
  const [temperature, setTemperature] = useState(0);
  const [maxTokens, setMaxTokens] = useState(500);

  const askQuestion = async () => {
    const response = await axios.post('http://localhost:8000/chat/', {
      model,
      question,
      history,
      temperature,
      max_tokens: maxTokens,
    });
    setHistory(response.data.history);
    setQuestion('');
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <div className="flex justify-center items-center space-x-10">
        <div className="border border-gray-300 rounded-lg p-10 shadow-lg">
          <h2 className="font-bold text-lg">Settings</h2>
          <label className="block mt-4">
            <span>Model:</span>
            <select value={model} onChange={(e) => setModel(e.target.value)}>
              <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
              <option value="gpt-4">gpt-4</option>
            </select>
          </label>
          <div className="block mt-4">
            <span>Temperature: {temperature}</span>
            <input
              type="range"
              min="0"
              max="1"
              step="0.01"
              value={temperature}
              onChange={(e) => setTemperature(+e.target.value)}
            />
          </div>
          <div className="block mt-4">
            <span>Tokens: {maxTokens}</span>
            <input
              type="range"
              min="256"
              max="3000"
              step="1"
              value={maxTokens}
              onChange={(e) => setMaxTokens(+e.target.value)}
            />
          </div>
        </div>
        <div className="border border-gray-300 rounded-lg p-10 shadow-lg max-w-md">
          <div className="flex flex-col items-center justify-center">
            <h1 className="text-3xl font-bold">Chat with your brain</h1>
            <h2 className="opacity-50">Your AI assistant</h2>
          </div>
          <div className="mt-5">
            {history.map(([speaker, text], idx) => (
              <p key={idx}>
                <b>{speaker}:</b> {text}
              </p>
            ))}
          </div>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="w-full p-2 mt-5 border border-gray-300 rounded"
            placeholder="Enter your question here..."
          />
          <button
            onClick={askQuestion}
            className="w-full mt-2 px-4 py-2 bg-blue-500 text-white rounded"
          >
            Ask
          </button>
        </div>
      </div>
    </div>
  );
}