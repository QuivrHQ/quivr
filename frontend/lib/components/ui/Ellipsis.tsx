/* eslint-disable */
"use client";
import { HTMLAttributes } from "react";

import { cn } from "@/lib/utils";

import Tooltip from "./Tooltip/Tooltip";

interface EllipsisProps extends HTMLAttributes<HTMLDivElement> {
  children: string;
  maxCharacters: number;
  tooltip?: boolean;
}

const Ellipsis = ({
  children: originalContent,
  className,
  maxCharacters,
  tooltip = false,
}: EllipsisProps): JSX.Element => {
  const renderedContent =
    originalContent.length > maxCharacters
      ? `${originalContent.slice(0, maxCharacters)}...`
      : originalContent;

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
