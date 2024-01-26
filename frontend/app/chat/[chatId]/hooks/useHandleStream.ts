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
    let incompleteData = "";

    const handleStreamRecursively = async () => {
      const { done, value } = await reader.read();

      if (done) {

	if (incompleteData !== "") {
          // Try to parse any remaining incomplete data

          try {
            const parsedData = JSON.parse(incompleteData) as ChatMessage;
            updateStreamingHistory(parsedData);
          } catch (e) {
            console.error("Error parsing incomplete data", e);
          }
        }

        return;
      }

      if (isFirstChunk) {
        isFirstChunk = false;
        onFirstChunk();
      }

      // Concatenate incomplete data with new chunk
      const rawData = incompleteData + decoder.decode(value, { stream: true });

      console.log("Raw data before cleaning:", rawData);

      const dataStrings = rawData
        .trim()
        .split("data: ")
        .filter(Boolean);

      dataStrings.forEach((data, index, array) => {
        if (index === array.length - 1 && !data.endsWith("\n")) {
          // Last item and does not end with a newline, save as incomplete
          incompleteData = data;

          return;
        }

        try {
          const parsedData = JSON.parse(data) as ChatMessage;
          updateStreamingHistory(parsedData);
        } catch (e) {
          console.error("Error parsing data string", e);
        }
      });

      await handleStreamRecursively();
    };

    await handleStreamRecursively();
  };

  return {
    handleStream,
  };
};

