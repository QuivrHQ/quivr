import Link from "next/link";
import { usePathname } from "next/navigation";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const StudioButton = (): JSX.Element => {
  const pathname = usePathname();
  const isSelected = pathname ? pathname.includes("/studio") : false;

  return (
    <Link href={`/studio`}>
      <MenuButton
        label="Brain Studio"
        isSelected={isSelected}
        iconName="brainCircuit"
        type="open"
        color="primary"
      />
    </Link>
  );
};
