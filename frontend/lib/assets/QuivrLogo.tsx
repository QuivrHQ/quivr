import Image from "next/image";

interface QuivrLogoProps {
  size: number;
  color?: "white" | "black" | "primary" | "accent";
}

export const QuivrLogo = ({ size }: QuivrLogoProps): JSX.Element => {
  return (
    <Image src="/logo-white.png" alt="Quivr Logo" width={size} height={size} />
  );
};
