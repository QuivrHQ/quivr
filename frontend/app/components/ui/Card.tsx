"use client";
import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import { FC, HTMLAttributes, LegacyRef, forwardRef } from "react";

type CardProps = HTMLAttributes<HTMLDivElement>;

const Card: FC<CardProps> = forwardRef(
  ({ children, className, ...props }, ref) => {
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
