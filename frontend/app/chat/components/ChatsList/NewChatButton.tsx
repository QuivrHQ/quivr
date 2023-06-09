import Link from "next/link";
import { BsPlusSquare } from "react-icons/bs";

export const NewChatButton = () => (
  <Link href="/chat">
    <button
      type="button"
      className="w-full mb-4 pl-4 pr-4 py-2 bg-gray-400 text-white rounded-lg flex items-center justify-center"
    >
      <BsPlusSquare className="h-6 w-6 mr-2" /> New Chat
    </button>
  </Link>
);
