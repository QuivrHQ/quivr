import Link from "next/link";
import { usePathname } from "next/navigation";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const KnowledgeButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/knowledge");

  return (
    <Link href={`/knowledge`}>
      <MenuButton
        label="My Knowledge"
        isSelected={isSelected}
        iconName="knowledge"
        type="open"
        color="primary"
      />
    </Link>
  );
};
