'use client';
import { useState, useEffect } from 'react';
import axios from 'axios';

interface Document {
    name: string;
    size: string;
}

export default function ExplorePage() {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);

    useEffect(() => {
        fetchDocuments();
    }, []);

    const fetchDocuments = async () => {
        try {
            const response = await axios.get<{ documents: Document[] }>('http://localhost:8000/explore');
            setDocuments(response.data.documents);
        } catch (error) {
            console.error('Error fetching documents', error);
            setDocuments([]);
        }
    };

    const viewDocument = (document: Document) => {
        setSelectedDocument(document);
    };

    return (
        <div className="pt-20 flex flex-col items-center justify-center p-6">
            <h1 className="text-4xl mb-6">Explore Files</h1>
            {documents.map((document, index) => (
                <div
                    key={index}
                    className="flex items-center justify-between w-1/2 p-4 mb-4 bg-white shadow rounded">
                    <p className="text-lg">{document.name}</p>
                    <button
                        onClick={() => viewDocument(document)}
                        className="py-2 px-4 bg-blue-500 text-white rounded mr-2 hover:bg-blue-600 transition duration-200">
                        View
                    </button>
                </div>
            ))}
            {selectedDocument && (
                <div className="fixed inset-0 flex items-center justify-center z-10">
                    <div className="bg-white p-6 w-1/2 h-1/2 overflow-auto">
                        <h2 className="text-2xl mb-4">{selectedDocument.name}</h2>
                        <pre>{JSON.stringify(selectedDocument, null, 2)}</pre>
                        <button onClick={() => setSelectedDocument(null)}>Close</button>
                    </div>
                </div>
            )}
        </div>
    );
}