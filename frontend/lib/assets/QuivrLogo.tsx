import Image from "next/image";

interface QuivrLogoProps {
  size: number;
  color?: "white" | "black" | "primary";
}

export const QuivrLogo = ({
  size,
  color = "white",
}: QuivrLogoProps): JSX.Element => {
  const filter = color === "black" ? "invert(1)" : "none";

  return (
    <Image
      src={"/vt-logo.png"}
      alt="Quivr Logo"
      width={size}
      height={size}
      style={{ filter }}
      className="rounded-full h-8 w-8"
    />
  );
};
