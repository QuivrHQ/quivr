import { HtmlHTMLAttributes } from "react";

import { cn } from "@/lib/utils";

type StyledFeedItemDivProps = HtmlHTMLAttributes<HTMLDivElement>;
export const StyledFeedItemDiv = ({
  className,
  ...propsWithoutClassname
}: StyledFeedItemDivProps): JSX.Element => (
  <div
    {...propsWithoutClassname}
    className={cn(
      "bg-gray-100 p-4 flex flex-row items-center py-2 rounded-lg shadow-sm",
      className
    )}
  />
);
