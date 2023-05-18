"use client";
import { FC, useEffect, useState } from "react";
import Button from "../ui/Button";
import { MdDarkMode, MdLightMode } from "react-icons/md";

interface DarkModeToggleProps {}

const DarkModeToggle: FC<DarkModeToggleProps> = ({}) => {
  const [dark, setDark] = useState(false);

  useEffect(() => {
    if (dark) {
      document.body.parentElement?.classList.add("dark");
    } else {
      document.body.parentElement?.classList.remove("dark");
    }
  }, [dark]);

  return (
    <Button
      aria-label="toggle dark mode"
      className="focus:outline-none"
      onClick={() => setDark((d) => !d)}
      variant={"tertiary"}
    >
      {dark ? <MdDarkMode /> : <MdLightMode />}
    </Button>
  );
};

export default DarkModeToggle;
