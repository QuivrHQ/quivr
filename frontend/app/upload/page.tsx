"use client";
import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";
import { Message } from "@/lib/types";

export default function UploadPage() {
    const [message, setMessage] = useState<Message | null>(null);

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        const file = acceptedFiles[0];
        const formData = new FormData();
        formData.append("file", file);
        try {
            const response = await axios.post(
                "http://localhost:8000/upload",
                formData
            );
            setMessage({
                type: "success",
                text:
                    "File uploaded successfully: " +
                    JSON.stringify(response.data),
            });
        } catch (error: any) {
            setMessage({
                type: "error",
                text: "Failed to upload file: " + error.toString(),
            });
        }
    }, []);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
    });

    return (
        <div
            {...getRootProps()}
            className="flex flex-col items-center justify-center h-screen bg-gray-100"
        >
            <input {...getInputProps()} />
            <div className="mt-2 p-6 max-w-sm mx-auto bg-white rounded-xl shadow-md flex items-center space-x-4">
                {isDragActive ? (
                    <p className="text-blue-600">Drop the files here...</p>
                ) : (
                    <p className="text-gray-500">
                        Drag 'n' drop some files here, or click to select files
                    </p>
                )}
            </div>
            {message && (
                <div
                    className={`mt-4 p-2 rounded ${
                        message.type === "success"
                            ? "bg-green-500"
                            : "bg-red-500"
                    }`}
                >
                    <p className="text-white">{message.text}</p>
                </div>
            )}
        </div>
    );
}
