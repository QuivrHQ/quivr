import Image from "next/image";

import { cn } from "@/lib/utils";

type AvatarProps = {
  url: string;
  imgClassName?: string;
  className?: string;
};
export const Avatar = ({
  url,
  imgClassName,
  className,
}: AvatarProps): JSX.Element => {
  return (
    <div className={cn("relative w-8 h-8 shrink-0", className)}>
      <Image
        alt="avatar"
        fill={true}
        sizes="32px"
        src={url}
        className={cn("rounded-xl", imgClassName)}
      />
    </div>
  );
};
