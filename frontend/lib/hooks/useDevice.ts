import { useEffect, useState } from "react";

// Max width for mobile device: 640px
// Match small min-width media query in tailwind
const MOBILE_MAX_WIDTH = 640;

export const useDevice = (): { isMobile: boolean } => {
  const [isMobile, setIsMobile] = useState(true);

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
