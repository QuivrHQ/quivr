"use client";
import Link from "next/link";
import { MdMic, MdMicOff, MdSettings } from "react-icons/md";
import Button from "../components/ui/Button";
import Card from "../components/ui/Card";
import PageHeading from "../components/ui/PageHeading";
import ChatMessages from "./components/ChatMessages";
import { useQuestion } from "./hooks/useQuestion";
import { useSpeech } from "./hooks/useSpeech";

export default function ChatPage() {
  const { history, isPending, question, askQuestion, setQuestion } =
    useQuestion();
  const { isListening, speechSupported, startListening } = useSpeech();

  return (
    <main className="min-h-0 w-full flex flex-col pt-32 flex-1 overflow-hidden">
      <section className="flex flex-col justify-center items-center gap-5 h-full overflow-auto style={{ marginBottom: '20px'}}">
        <PageHeading
          title="Chat with your brain"
          subtitle="Talk to a language model about your uploaded data"
        />
        {/* Chat */}
        <Card className="p-5 max-w-3xl w-full flex-1 mb-24 overflow-auto flex flex-col">
          <ChatMessages history={history} />
        </Card>
        <Card className="fixed left-1/2 w-full max-w-3xl bg-gray-100 dark:bg-gray-800 rounded-b-none -translate-x-1/2 bottom-16 px-5 py-5">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              if (!isPending) askQuestion();
            }}
            className="w-full flex items-center justify-center gap-2"
          >
            <textarea
              autoFocus
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault(); // Prevents the newline from being entered in the textarea
                  if (!isPending) askQuestion(); // Call the submit function here
                }
              }}
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
              onClick={startListening}
              disabled={!speechSupported}
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
      </section>
    </main>
  );
}
