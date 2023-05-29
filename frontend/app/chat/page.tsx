"use client";
import axios from "axios";
import { redirect } from "next/navigation";
import { useEffect, useState } from "react";
import { MdMic, MdMicOff, MdSettings } from "react-icons/md";
import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import Modal from "../components/ui/Modal";
import PageHeading from "../components/ui/PageHeading";
import { useSupabase } from "../supabase-provider";
import ChatMessages from "./ChatMessages";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<Array<[string, string]>>([]);
  const [model, setModel] = useState("gpt-3.5-turbo");
  const [temperature, setTemperature] = useState(0);
  const [maxTokens, setMaxTokens] = useState(500);
  const [isPending, setIsPending] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const { session } = useSupabase();
  if (session === null) {
    redirect("/login");
  }

  useEffect(() => {
    if (typeof window !== "undefined") {
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
    const response = await axios.post(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/chat/`,
      {
        model,
        question,
        history,
        temperature,
        max_tokens: maxTokens,
      },
      {
        headers: {
          Authorization: `Bearer ${session.access_token}`,
        },
      }
    );
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
              >
                {isListening ? (
                  <MdMicOff className="text-2xl" />
                ) : (
                  <MdMic className="text-2xl" />
                )}
              </Button>
              {/* Settings Button */}
              <Modal
                Trigger={
                  <Button className="px-3" variant={"tertiary"}>
                    <MdSettings className="text-2xl" />
                  </Button>
                }
                title="Settings"
                desc="Modify your brain"
              >
                <form className="flex flex-col gap-5 py-5">
                  <fieldset className="w-full flex">
                    <label className="flex-1" htmlFor="model">
                      Model:
                    </label>
                    <select
                      name="model"
                      id="model"
                      value={model}
                      className="px-5 py-2 dark:bg-gray-700 bg-gray-200 rounded-md"
                      onChange={(e) => setModel(e.target.value)}
                    >
                      <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
                      <option value="gpt-4">gpt-4</option>
                    </select>
                  </fieldset>
                  <fieldset className="w-full flex">
                    <label className="flex-1" htmlFor="temp">
                      Temperature: {temperature}
                    </label>
                    <input
                      name="temp"
                      id="temp"
                      type="range"
                      min="0"
                      max="1"
                      step="0.01"
                      value={temperature}
                      onChange={(e) => setTemperature(+e.target.value)}
                    />
                  </fieldset>
                  <fieldset className="w-full flex">
                    <label className="flex-1" htmlFor="tokens">
                      Tokens: {maxTokens}
                    </label>
                    <input
                      name="tokens"
                      id="tokens"
                      type="range"
                      min="256"
                      max="3000"
                      step="1"
                      value={maxTokens}
                      onChange={(e) => setMaxTokens(+e.target.value)}
                    />
                  </fieldset>
                </form>
              </Modal>
            </form>
          </Card>
        </Card>
      </section>
    </main>
  );
}
