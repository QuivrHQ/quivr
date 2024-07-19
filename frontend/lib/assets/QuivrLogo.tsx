import Image from "next/image";
import { useEffect, useState } from "react";

interface QuivrLogoProps {
  size: number;
  color?: "white" | "black" | "primary" | "accent";
}

export const QuivrLogo = ({
  size,
  color = "white",
}: QuivrLogoProps): JSX.Element => {
  const [src, setSrc] = useState<string>("/logo-white.svg");

  useEffect(() => {
    if (color === "primary") {
      setSrc("/logo-primary.svg");
    } else if (color === "accent") {
      setSrc("/logo-accent.svg");
    } else if (color === "black") {
      setSrc("/logo-black.svg");
    } else {
      setSrc("/logo-white.svg");
    }
  }, [color]);

  return <Image src={src} alt="Quivr Logo" width={size} height={size} />;
};
