import { useEffect, useLayoutEffect, useState } from "react";

export type Theme = "dark" | "light" | "system";

/**
 * @todo implement "system" theme
 */
export const useTheme = (): {
  isDark: boolean;
  isLight: boolean;
  theme: Theme;
  setTheme: (t: Theme) => void;
} => {
  const [theme, setTheme] = useState<Theme>("light");
  const isDark = theme === "dark";
  const isLight = theme === "light";

  useLayoutEffect(() => {
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
      document.body.parentElement?.classList.add("dark");

      setTheme(savedTheme);
    }
  }, []);

  useEffect(() => {
    if (isDark) {
      document.body.parentElement?.classList.add("dark");
    } else {
      document.body.parentElement?.classList.remove("dark");
    }

    localStorage.setItem("theme", theme);
  }, [theme, isDark]);

  return {
    isDark,
    isLight,
    theme,
    setTheme,
  };
};
