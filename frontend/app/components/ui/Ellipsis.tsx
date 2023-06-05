"use client";
import { cn } from "@/lib/utils";
import { FC, HTMLAttributes } from "react";
import Tooltip from "./Tooltip";

interface EllipsisProps extends HTMLAttributes<HTMLDivElement> {
  children: string;
  maxCharacters: number;
  tooltip?: boolean;
}

const Ellipsis: FC<EllipsisProps> = ({
  children: originalContent,
  className,
  maxCharacters,
  tooltip = false,
}) => {
  const renderedContent =
    originalContent.length > maxCharacters
      ? `${originalContent.slice(0, maxCharacters)}...`
      : originalContent;
  console.log(originalContent, maxCharacters, tooltip, renderedContent);

  if (tooltip && originalContent !== renderedContent) {
    return (
      <Tooltip tooltip={originalContent}>
        <span aria-label={originalContent} className={cn("", className)}>
          {renderedContent}
        </span>
      </Tooltip>
    );
  }

  return (
    <span aria-label={originalContent} className={cn("", className)}>
      {renderedContent}
    </span>
  );
};

export default Ellipsis;
