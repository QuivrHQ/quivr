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

export const AnimatedCard = motion(Card);
AnimatedCard.displayName = "AnimatedCard";
Card.displayName = "Card";
export default Card;
