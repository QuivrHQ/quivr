import Image from "next/image";

interface QuivrLogoProps {
  size: number;
  color?: "white" | "black" | "primary" | "accent";
}

export const QuivrLogo = ({
  size,
  color = "white",
}: QuivrLogoProps): JSX.Element => {
  let src = "/logo-white.svg";
  if (color === "primary") {
    src = "/logo-primary.svg";
  } else if (color === "accent") {
    src = "/logo-accent.svg";
  }

  const filter = color === "black" ? "invert(1)" : "none";

  return (
    <Image
      src={src}
      alt="Quivr Logo"
      width={size}
      height={size}
      style={{ filter }}
    />
  );
};
