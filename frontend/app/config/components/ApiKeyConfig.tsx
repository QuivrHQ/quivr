/* eslint-disable */
"use client";

import { useState } from "react";

import Button from "@/lib/components/ui/Button";
import { useAxios } from "@/lib/useAxios";

export const ApiKeyConfig = (): JSX.Element => {
  const [apiKey, setApiKey] = useState("");
  const { axiosInstance } = useAxios();

  const handleCreateClick = async () => {
    try {
      const response = await axiosInstance.post("/api-key"); // replace with your api-key endpoint URL
      setApiKey(response.data.api_key);
    } catch (error) {
      console.error("Error creating API key: ", error);
    }
  };

  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  const handleCopyClick = () => {
    if (apiKey) {
      copyToClipboard(apiKey);
    }
  };

  return (
    <>
      <div className="border-b border-gray-300 w-full max-w-xl mb-8">
        <p className="text-center text-gray-600 uppercase tracking-wide font-semibold">
          API Key Config
        </p>
      </div>
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-4">
          {apiKey === "" && (
            <Button variant="secondary" onClick={handleCreateClick}>
              Create New Key
            </Button>
          )}
        </div>
        {apiKey !== "" && (
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">{apiKey}</span>
            <Button variant="secondary" onClick={handleCopyClick}>
              📋
            </Button>
          </div>
        )}
      </div>
    </>
  );
};
