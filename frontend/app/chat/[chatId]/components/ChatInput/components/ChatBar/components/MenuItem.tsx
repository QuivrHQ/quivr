"use client";
import { BeautifulMentionsMenuItemProps } from "lexical-beautiful-mentions";
import { forwardRef } from "react";

import Button from "@/lib/components/ui/Button";
import { cn } from "@/lib/utils";

export const MenuItem = forwardRef<
  HTMLLIElement,
  BeautifulMentionsMenuItemProps
>(({ selected, itemValue, label, ...props }, ref) => (
  <li
    ref={ref}
    className={cn(
      "m-0 flex min-w-[150px] shrink-0 cursor-pointer flex-row content-center whitespace-nowrap border-0 px-2.5 py-2 leading-4 text-slate-950 outline-none first:mt-1.5 last:mb-1.5 dark:text-slate-300",
      selected ? "bg-gray-100 dark:bg-gray-700" : "bg-white dark:bg-gray-900"
    )}
    {...props}
  >
    <div>
      {label}
      <Button
        onClick={(e) => {
          e.preventDefault();
          e.stopPropagation();
          alert("delete");
        }}
      >
        Delete
      </Button>
    </div>
  </li>
));
