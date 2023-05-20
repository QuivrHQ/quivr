"use client";
import { useState } from "react";
import axios from "axios";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Modal from "../components/ui/Modal";
import { MdSettings } from "react-icons/md";
import ChatMessages from "./ChatMessages";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [history, setHistory] = useState<Array<[string, string]>>([
    // ["user", "Hello!"],
    // ["assistant", "Hello Back!"],
    // ["user", "Send some long message"],
    // [
    //   "assistant",
    //   "This is a very long and really long message which is longer than every other message.",
    // ],
    // ["user", "What is redux"],
    // ["assistant", ``],
  ]);
  const [model, setModel] = useState("gpt-3.5-turbo");
  const [temperature, setTemperature] = useState(0);
  const [maxTokens, setMaxTokens] = useState(500);
  const [isPending, setIsPending] = useState(false);

  const askQuestion = async () => {
    setHistory((hist) => [...hist, ["user", question]]);
    setIsPending(true);
    const response = await axios.post("http://localhost:8000/chat/", {
      model,
      question,
      history,
      temperature,
      max_tokens: maxTokens,
    });
    setHistory(response.data.history);
    console.log(response.data.history);

    setQuestion("");
    setIsPending(false);
  };

  return (
    <div className="min-h-screen w-full pt-24">
      <div className="flex flex-col justify-center items-center gap-5">
        {/* Chat */}
        <div className="flex flex-col items-center justify-center">
          <h1 className="text-3xl font-bold text-center">
            Chat with your brain
          </h1>
          <h2 className="opacity-50">Your AI assistant</h2>
        </div>
        <Card className="p-10 max-w-3xl">
          <ChatMessages history={history} />
          <Card className="fixed left-1/2 w-full max-w-4xl -translate-x-1/2 bottom-0 p-10">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                askQuestion();
              }}
              className="w-full flex items-center justify-center"
            >
              <input
                autoFocus
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="w-full p-2 border border-gray-300 dark:border-gray-500 outline-none rounded dark:bg-gray-800"
                placeholder="Enter your question here..."
              />
              <Button type="submit" isLoading={isPending}>
                {isPending ? "Thinking..." : "Ask"}
              </Button>
            </form>
          </Card>
        </Card>

        {/* Settings Modal */}
        <Modal
          Trigger={
            <Button className="" variant={"secondary"}>
              Settings <MdSettings className="text-2xl" />
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
      </div>
    </div>
  );
}
