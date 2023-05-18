'use client';
import { useState } from 'react';
import axios from 'axios';

export default function ChatPage() {
  const [question, setQuestion] = useState('');
  const [history, setHistory] = useState([['User', 'Hello!']]);

  const askQuestion = async () => {
    const response = await axios.post('http://localhost:8000/chat/', {
      model: 'gpt-3.5-turbo',
      question,
      history
    });
    setHistory(response.data.history);
    setQuestion('');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-200 py-2">
      <div className="px-4 py-5 bg-white shadow rounded-lg w-full md:w-1/2">
        {history.map(([speaker, text], idx) => (
          <p key={idx} className="mb-4 text-black">
            <b className="mr-2 text-black">{speaker}:</b> {text}
          </p>
        ))}
      </div>
      <div className="mt-6">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="px-3 py-2 border border-gray-300 shadow-sm rounded-md focus:outline-none text-black focus:ring-2 focus:ring-indigo-600"
        />
        <button onClick={askQuestion} className="ml-2 px-4 py-2 bg-indigo-600 text-white rounded-md shadow-sm hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          Ask
        </button>
      </div>
    </div>
  );
}
