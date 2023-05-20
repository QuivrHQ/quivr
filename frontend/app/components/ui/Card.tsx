import { cn } from "@/lib/utils";
import { FC, HTMLAttributes } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {}

const Card: FC<CardProps> = ({ children, className, ...props }) => {
  return (
    <div
      className={cn(
        "shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden bg-white dark:bg-black border border-black/10 dark:border-white/25",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};

export default Card;
