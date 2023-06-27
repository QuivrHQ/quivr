import Link from "next/link";
import { BsPlusSquare } from "react-icons/bs";

export const NewChatButton = (): JSX.Element => (
  <Link
    href="/chat"
    className="px-4 py-2 mx-4 my-1 border border-primary bg-white dark:bg-black hover:text-white hover:bg-primary shadow-lg rounded-lg flex items-center justify-center top-1 z-20"
  >
    <BsPlusSquare className="h-6 w-6 mr-2" /> New Chat
  </Link>
);
