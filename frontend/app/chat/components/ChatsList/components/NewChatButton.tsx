import Link from "next/link";
import { useTranslation } from "react-i18next";
import { BsPlusSquare } from "react-icons/bs";

const newChatRoute = "/chat";
export const NewChatButton = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Link
      href={newChatRoute}
      data-testid="new-chat-button"
      className="px-4 py-2 mx-4 my-1 border border-primary bg-white dark:bg-black hover:text-white hover:bg-primary shadow-lg rounded-lg flex items-center justify-center top-1 z-20"
    >
      <BsPlusSquare className="h-6 w-6 mr-2" /> {t("newChatButton")}
    </Link>
  );
};
