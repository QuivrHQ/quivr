import { redirect } from "next/navigation";

export const redirectToPreviousPageOrChatPage = (): void => {
  const previousPage = sessionStorage.getItem("previous-page");
  if (previousPage === null) {
    redirect("/chat");
  } else {
    sessionStorage.removeItem("previous-page");
    redirect(previousPage);
  }
};
