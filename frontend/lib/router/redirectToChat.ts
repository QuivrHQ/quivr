"use client";

import { RedirectType } from "next/dist/client/components/redirect";
import { redirect } from "next/navigation";

type redirectToChat = (type?: RedirectType) => never;

export const redirectToChat: redirectToChat = (type?: RedirectType) => {
  sessionStorage.setItem("previous-page", window.location.pathname);

  redirect("/chat", type);
};
