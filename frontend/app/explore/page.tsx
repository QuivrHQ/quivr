'use client';
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function ExplorePage() {
    const [files, setFiles] = useState([]);
    const [selectedFile, setSelectedFile] = useState(null);

    useEffect(() => {
        fetchFiles();
    }, []);

    const fetchFiles = async () => {
        try {
            const response = await axios.get('http://localhost:8000/explore');
            if (Array.isArray(response.data.documents)) {
                setFiles(response.data.documents);
            } else {
                console.error('Unexpected data structure', response.data);
            }
        } catch (error) {
            console.error('Error fetching files', error);
        }
    };

    const deleteFile = async (filename) => {
        await axios.delete(`http://localhost:8000/explore/${filename}`);
        fetchFiles();
    };

    const viewFile = async (filename) => {
        const response = await axios.get(`http://localhost:8000/explore/${filename}`);
        if (response.data && Array.isArray(response.data.documents)) {
            setSelectedFile({
                name: filename,
                documents: response.data.documents
            });
        } else {
            console.error('Unexpected data structure', response.data);
        }
    };

    return (
        <div className="pt-20 flex flex-col items-center justify-center p-6">
            <h1 className="text-4xl mb-6">Explore Files</h1>
            {files.map((file, index) => (
                <div
                    key={index}
                    className="flex items-center justify-between w-1/2 p-4 mb-4 bg-white shadow rounded">
                    <p className="text-lg">{file.name}</p>
                    <div>
                        <button
                            onClick={() => viewFile(file.name)}
                            className="py-2 px-4 bg-blue-500 text-white rounded mr-2 hover:bg-blue-600 transition duration-200">
                            View
                        </button>
                        <button
                            onClick={() => deleteFile(file.name)}
                            className="py-2 px-4 bg-red-500 text-white rounded hover:bg-red-600 transition duration-200">
                            Delete
                        </button>
                    </div>
                </div>
            ))}
            {selectedFile && (
                <div className="fixed inset-0 flex items-center justify-center z-10">
                    <div className="bg-white p-6 w-1/2 h-1/2 overflow-auto">
                        <h2 className="text-2xl mb-4">{selectedFile.name}</h2>
                        {selectedFile.documents.map((document, index) => (
                            <div key={index}>
                                <pre>{JSON.stringify(document, null, 2)}</pre>
                            </div>
                        ))}
                        <button onClick={() => setSelectedFile(null)}>Close</button>
                    </div>
                </div>
            )}
        </div>
    );
}
