'use client';
import { useState, useEffect } from 'react';
import axios from 'axios';
import DocumentItem from './documentItem';

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
            console.log(`Fetching documents from ${process.env.NEXT_PUBLIC_BACKEND_URL}/explore`);
            const response = await axios.get<{ documents: Document[] }>(`${process.env.NEXT_PUBLIC_BACKEND_URL}/explore`);
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
            <div className="overflow-y-auto h-[50vh] w-full max-w-xl">
                {documents.map((document, index) => (
                    <DocumentItem key={index} document={document} viewDocument={viewDocument} />
                ))}
            </div>
            {selectedDocument && (
                <div className="fixed inset-0 flex items-center justify-center z-10 bg-black bg-opacity-50">
                    <div className="bg-white p-6 w-1/2 h-1/2 overflow-auto rounded-lg">
                        <h2 className="text-2xl mb-4">{selectedDocument.name}</h2>
                        <pre>{JSON.stringify(selectedDocument, null, 2)}</pre>
                        <button 
                            onClick={() => setSelectedDocument(null)}
                            className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition duration-200"
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
