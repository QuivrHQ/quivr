import Link from "next/link";
import { BsPlusSquare } from "react-icons/bs";

export const NewChatButton = () => (
  <Link
    href="/chat"
    className="px-4 py-2 mx-4 my-2 border border-primary hover:text-white hover:bg-primary shadow-lg rounded-lg flex items-center justify-center"
  >
    <BsPlusSquare className="h-6 w-6 mr-2" /> New Chat
  </Link>
);
