import { forwardRef } from "react";

import { TabsTrigger } from "@/lib/components/ui/Tabs";
import { cn } from "@/lib/utils";

export const StyledTabsTrigger = forwardRef<
  React.ElementRef<typeof TabsTrigger>,
  React.ComponentPropsWithoutRef<typeof TabsTrigger>
>(({ className, ...props }, ref) => (
  <TabsTrigger
    ref={ref}
    className={cn(
      "capitalize font-normal",
      "data-[state=active]:shadow-none",
      "data-[state=active]:text-primary",
      "data-[state=active]:font-semibold",
      className
    )}
    {...props}
  />
));
StyledTabsTrigger.displayName = TabsTrigger.displayName;
