import { useEffect, useState } from "react";

const MOBILE_MAX_WIDTH = 576;

export const useDevice = (): { isMobile: boolean } => {
  const [isMobile, setIsMobile] = useState(
    window.innerWidth < MOBILE_MAX_WIDTH
  );

  useEffect(() => {
    const handleResize = () => {
      const screenWidth = window.innerWidth;
      setIsMobile(screenWidth < MOBILE_MAX_WIDTH);
    };

    // Initial check
    handleResize();

    // Event listener for screen resize
    window.addEventListener("resize", handleResize);

    // Clean up event listener on component unmount
    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return { isMobile };
};
