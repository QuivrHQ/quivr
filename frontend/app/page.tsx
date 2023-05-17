'use client';
import Link from 'next/link';

export default function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="m-4 p-6 max-w-md mx-auto bg-white rounded-xl shadow-md flex items-center space-x-4">
        <h1 className="mb-4 text-xl font-bold text-gray-900">Welcome!</h1>
        <div className="flex flex-col space-y-4">
          <Link
            href="/chat"
            className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
            
              Go to Chat
            
          </Link>
          <Link
            href="/upload"
            className="px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700">
            
              Go to Upload
            
          </Link>
        </div>
      </div>
    </div>
  );
}