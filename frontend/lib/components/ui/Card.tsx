/* eslint-disable */
"use client";
import { motion } from "framer-motion";
import { forwardRef, HTMLAttributes, LegacyRef } from "react";

import { cn } from "@/lib/utils";

type CardProps = HTMLAttributes<HTMLDivElement>;

const Card = forwardRef(
  ({ children, className, ...props }: CardProps, ref): JSX.Element => {
    return (
      <div
        ref={ref as LegacyRef<HTMLDivElement>}
        className={cn(
          "shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden bg-white dark:bg-black border border-black/10 dark:border-white/25",
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

type CardChildProps = HTMLAttributes<HTMLDivElement>;

const CardHeader = ({ children, className }: CardChildProps) => {
  return <div className={cn("border-b p-3", className)}>{children}</div>;
};
CardHeader.displayName = "CardHeader";

const CardBody = ({ children, className }: CardChildProps) => {
  return <div className={cn("p-3", className)}>{children}</div>;
};
CardBody.displayName = "CardHeader";

const CardFooter = ({ children, className }: CardChildProps) => {
  return <div className={cn("border-t p-3", className)}>{children}</div>;
};
CardFooter.displayName = "CardHeader";

export { CardBody, CardFooter, CardHeader };

export const AnimatedCard = motion(Card);
AnimatedCard.displayName = "AnimatedCard";
Card.displayName = "Card";
export default Card;
