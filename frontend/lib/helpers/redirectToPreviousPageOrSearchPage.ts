import { redirect } from "next/navigation";

export const redirectToPreviousPageOrSearchPage = (): void => {
  const previousPage = sessionStorage.getItem("previous-page");
  if (previousPage === null) {
    redirect("/search");
  } else {
    sessionStorage.removeItem("previous-page");
    redirect(previousPage);
  }
};
