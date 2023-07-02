"use client";

import useLocalStorage from "@/lib/hooks/use-local-storage";
import { defaultFontMapper, displayFontMapper } from "@/styles/fonts";
import { Analytics } from "@vercel/analytics/react";
import clsx from "clsx";
import { Dispatch, ReactNode, SetStateAction, createContext } from "react";
import { Toaster } from "sonner";

export const AppContext = createContext<{
  font: string;
  setFont: Dispatch<SetStateAction<string>>;
}>({
  font: "Sans Serif",
  setFont: () => {},
});

export default function Providers({ children }: { children: ReactNode }) {
  const [font, setFont] = useLocalStorage<string>("novel__font", "Sans Serif");

  return (
    <AppContext.Provider
      value={{
        font,
        setFont,
      }}
    >
      <Toaster />
      <body className={clsx(displayFontMapper[font], defaultFontMapper[font])}>
        {children}
      </body>
      <Analytics />
    </AppContext.Provider>
  );
}
