"use client";
import { FC } from "react";
import Tooltip from "./Tooltip";

interface EllipsisProps {
  children: string;
  maxCharacters: number;
  tooltip?: boolean;
}

const Ellipsis: FC<EllipsisProps> = ({
  children: originalContent,
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
        <span aria-label={originalContent} className="">
          {renderedContent}
        </span>
      </Tooltip>
    );
  }

  return (
    <span aria-label={originalContent} className="">
      {renderedContent}
    </span>
  );
};

export default Ellipsis;
