import { useChatContext } from "@/lib/context";

import { ChatMessage } from "../types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useHandleStream = () => {
  const { updateStreamingHistory } = useChatContext();

  const handleStream = async (
    reader: ReadableStreamDefaultReader<Uint8Array>,
    onFirstChunk: () => void
  ): Promise<void> => {
    const decoder = new TextDecoder("utf-8");
    let isFirstChunk = true;

    const handleStreamRecursively = async () => {
      const { done, value } = await reader.read();

      if (done) {
        return;
      }

      if (isFirstChunk) {
        isFirstChunk = false;
        onFirstChunk();
      }

      const dataStrings = decoder
        .decode(value)
        .trim()
        .split("data: ")
        .filter(Boolean);

      dataStrings.forEach((data) => {
        const parsedData = JSON.parse(data) as ChatMessage;
        updateStreamingHistory(parsedData);
      });

      await handleStreamRecursively();
    };

    await handleStreamRecursively();
  };

  return {
    handleStream,
  };
};
