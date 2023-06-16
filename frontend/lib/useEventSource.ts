import {
  EventSourceMessage,
  fetchEventSource,
  FetchEventSource,
} from "@microsoft/fetch-event-source";

import { useSupabase } from "@/app/supabase-provider";

import { useBrainConfig } from "./context/BrainConfigProvider/hooks/useBrainConfig";

type EventSourceHook = {
  openStream: (
    url: string,
    options: Record<string, unknown>,
    onMessage: (data: unknown) => void,
    onError: (err: Event) => void,
    onClose?: () => void
  ) => () => void;
};

export const useEventSource = (): EventSourceHook => {
  const { session } = useSupabase();
  const {
    config: { backendUrl, openAiKey },
  } = useBrainConfig();

  const openStream: EventSourceHook["openStream"] = (
    url,
    options,
    onMessage,
    onError,
    onClose
  ) => {
    if (session == null) {
      console.error("No session available");

      return () => {};
    }

    let eventSource: FetchEventSource | null = null;

    //backendUrl is undefined :(
    console.log(backendUrl, url);

    try {
      eventSource = fetchEventSource(`http://localhost:5050${url}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${session.access_token ?? ""}`,
          "Openai-Api-Key": openAiKey ?? "",
          Expect: "text/event-stream",
        },
        body: JSON.stringify(options),
        onopen: (res: Response) => {
          if (res.ok && res.status === 200) {
            console.log("Connection made ", res);
          } else {
            console.log("Connection failed ", res);
          }
        },
        onmessage: (event: EventSourceMessage) => {
          console.log(event.data);
          const parsedData = JSON.parse(event.data);
          onMessage(parsedData);
        },
        onerror: (err: Event) => {
          console.error("There was an error from server", err);
          onError(err);
        },
        onclose: () => {
          console.log("Connection closed by the server");
          if (onClose) {
            onClose();
          }
        },
      });
    } catch (err) {
      console.error("Error establishing EventSource connection:", err);
    }

    return () => {
      if (eventSource !== null) {
        eventSource.close();
      }
    };
  };

  return {
    openStream,
  };
};
