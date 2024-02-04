import Link from "next/link";
import { usePathname } from "next/navigation";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const StudioButton = (): JSX.Element => {
  return (
    <Link href={`/studio`}>
      <MenuButton
        label="Studio"
        isSelected={usePathname()?.includes("/studio")}
        iconName="brainCircuit"
        type="open"
        color="primary"
      />
    </Link>
  );
};
