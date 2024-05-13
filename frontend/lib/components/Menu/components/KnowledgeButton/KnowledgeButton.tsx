import Link from "next/link";
import { usePathname } from "next/navigation";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const KnowledgeButton = (): JSX.Element => {
  const pathname = usePathname();
  const isSelected = pathname ? pathname.includes("/knowledge") : false;

  return (
    <Link href={`/knowledge`}>
      <MenuButton
        label="Knowledge"
        isSelected={isSelected}
        iconName="book"
        type="open"
        color="primary"
      />
    </Link>
  );
};
