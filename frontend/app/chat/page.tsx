"use client";
import { useBrainConfig } from "@/lib/context/BrainConfigProvider/hooks/useBrainConfig";
import { useAxios } from "@/lib/useAxios";
import Link from "next/link";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { MdMic, MdMicOff, MdSettings } from "react-icons/md";
import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import PageHeading from "../components/ui/PageHeading";
import { useSupabase } from "../supabase-provider";
import ChatMessages from "./ChatMessages";
import { isSpeechRecognitionSupported } from "./helpers";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<Array<[string, string]>>([]);
  const [isPending, setIsPending] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const { session } = useSupabase();
  const { axiosInstance } = useAxios();
  const {
    config: { maxTokens, model, temperature },
  } = useBrainConfig();
  if (session === null) {
    redirect("/login");
  }

  useEffect(() => {
    if (isSpeechRecognitionSupported()) {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;

      const mic = new SpeechRecognition();

      mic.continuous = true;
      mic.interimResults = false;
      mic.lang = "en-US";

      mic.onstart = () => {
        console.log("Mics on");
      };

      mic.onend = () => {
        console.log("Mics off");
      };

      mic.onerror = (event: SpeechRecognitionErrorEvent) => {
        console.log(event.error);
        setIsListening(false);
      };

      mic.onresult = (event: SpeechRecognitionEvent) => {
        const interimTranscript =
          event.results[event.results.length - 1][0].transcript;
        setQuestion((prevQuestion) => prevQuestion + interimTranscript);
      };

      if (isListening) {
        mic.start();
      }

      return () => {
        if (mic) {
          mic.stop();
        }
      };
    }
  }, [isListening]);

  const askQuestion = async () => {
    setHistory((hist) => [...hist, ["user", question]]);
    setIsPending(true);
    setIsListening(false);

    const response = await axiosInstance.post(`/chat/`, {
      model,
      question,
      history,
      temperature,
      max_tokens: maxTokens,
    });
    setHistory(response.data.history);
    setQuestion("");
    setIsPending(false);
  };

  const handleListen = () => {
    setIsListening((prevIsListening) => !prevIsListening);
  };

  return (
    <main className="min-h-screen w-full flex flex-col pt-32">
      <section className="flex flex-col justify-center items-center flex-1 gap-5 h-full">
        <PageHeading
          title="Chat with your brain"
          subtitle="Talk to a language model about your uploaded data"
        />
        {/* Chat */}
        <Card className="p-5 max-w-3xl w-full min-h-full flex-1 mb-24">
          <ChatMessages history={history} />
          <Card className="fixed left-1/2 w-full max-w-3xl bg-gray-100 dark:bg-gray-800 rounded-b-none -translate-x-1/2 bottom-0 px-5 py-5">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                if (!isPending) askQuestion();
              }}
              className="w-full flex items-center justify-center gap-2"
            >
              <input
                autoFocus
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="w-full p-2 border border-gray-300 dark:border-gray-500 outline-none rounded dark:bg-gray-800"
                placeholder="Begin conversation here..."
              />
              <Button type="submit" isLoading={isPending}>
                {isPending ? "Thinking..." : "Chat"}
              </Button>
              {/* Mic Button */}
              <Button
                className="px-3"
                variant={"tertiary"}
                type="button"
                onClick={handleListen}
                disabled={!isSpeechRecognitionSupported()}
              >
                {isListening ? (
                  <MdMicOff className="text-2xl" />
                ) : (
                  <MdMic className="text-2xl" />
                )}
              </Button>
              <Link href={"/config"}>
                <Button className="px-3" variant={"tertiary"}>
                  <MdSettings className="text-2xl" />
                </Button>
              </Link>
            </form>
          </Card>
        </Card>
      </section>
    </main>
  );
}
