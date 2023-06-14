/* eslint-disable */
import { useEffect, useRef, useState } from "react";

export const useHeader = () => {
  const [hidden, setHidden] = useState(false);
  const scrollPos = useRef<number>(0);

  useEffect(() => {
    const handleScroll = (e: Event) => {
      const target = e.currentTarget as Window;
      if (target.scrollY > scrollPos.current) {
        setHidden(true);
      } else {
        setHidden(false);
      }
      scrollPos.current = target.scrollY;
    };

    window.addEventListener("scroll", handleScroll);

    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return {
    hidden,
  };
};
