/* eslint-disable */
"use client";
import { MdDarkMode, MdLightMode } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { useTheme } from "./hooks/useTheme";

export const DarkModeToggle = (): JSX.Element => {
  const { isDark, setTheme } = useTheme();

  return (
    <Button
      aria-label="toggle dark mode"
      className="focus:outline-none text-3xl"
      onClick={() => setTheme(isDark ? "light" : "dark")}
      variant={"tertiary"}
    >
      {isDark ? <MdLightMode /> : <MdDarkMode />}
    </Button>
  );
};
