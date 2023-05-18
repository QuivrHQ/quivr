"use client";
import { FC, useEffect, useLayoutEffect, useState } from "react";
import Button from "../ui/Button";
import { MdDarkMode, MdLightMode } from "react-icons/md";

interface DarkModeToggleProps {}

const DarkModeToggle: FC<DarkModeToggleProps> = ({}) => {
  const [dark, setDark] = useState(false);

  useLayoutEffect(() => {
    const isDark = localStorage.getItem("dark");
    if (isDark && isDark === "true") {
      document.body.parentElement?.classList.add("dark");
      setDark(true);
    }
  }, []);

  useEffect(() => {
    if (dark) {
      document.body.parentElement?.classList.add("dark");
      localStorage.setItem("dark", "true");
    } else {
      document.body.parentElement?.classList.remove("dark");
      localStorage.setItem("dark", "false");
    }
  }, [dark]);

  return (
    <Button
      aria-label="toggle dark mode"
      className="focus:outline-none"
      onClick={() => setDark((d) => !d)}
      variant={"tertiary"}
    >
      {dark ? <MdLightMode /> : <MdDarkMode />}
    </Button>
  );
};

export default DarkModeToggle;
