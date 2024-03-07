import Image from "next/image";

interface LuccidLogoProps {
    size: number;
  }
    
export const LuccidLogo = ({size}: LuccidLogoProps): JSX.Element => {
  return (
    <Image
        src={"/logo.png"}
        alt="Luccid Logo"
        width={size}
        height={size}
    />
  );
};
