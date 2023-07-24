import { usePathname } from "next/navigation";

import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useBrainListItem = (brain: MinimalBrainForUser) => {
  const pathname = usePathname()?.split("/").at(-1);
  const selected = brain.id === pathname;

  return {
    selected,
  };
};
