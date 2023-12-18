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
      "capitalize",
      "data-[state=active]:shadow-none",
      "data-[state=active]:text-primary",
      className
    )}
    {...props}
  />
));
StyledTabsTrigger.displayName = TabsTrigger.displayName;
