import Image from "next/image";

import { cn } from "@/lib/utils";

type AvatarProps = {
  url: string;
  alt: string;
  imgClassName?: string;
  className?: string;
};
export const Avatar = ({
  url,
  alt,
  imgClassName,
  className,
}: AvatarProps): JSX.Element => {
  return (
    <div className={cn("relative w-8 h-8", className)}>
      <Image
        alt={alt}
        fill={true}
        sizes="32px"
        src={url}
        className={cn("rounded-xl", imgClassName)}
      />
    </div>
  );
};
