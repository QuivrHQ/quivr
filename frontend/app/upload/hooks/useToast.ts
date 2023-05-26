import { ToastRef } from "@/app/components/ui/Toast";
import { Message } from "postcss";
import { useEffect, useRef, useState } from "react";

export const useToast = () => {
  const [message, setMessage] = useState<Message | null>(null);
  const messageToast = useRef<ToastRef>(null);

  useEffect(() => {
    if (!message) return;
    messageToast.current?.publish({
      variant:
        message.type === "error"
          ? "danger"
          : message.type === "warning"
          ? "neutral"
          : "success",
      text: message.text,
    });
  }, [message]);
  return {
    setMessage,
    messageToast,
  };
};
