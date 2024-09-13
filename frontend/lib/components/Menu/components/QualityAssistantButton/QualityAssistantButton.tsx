import Link from "next/link";
import { usePathname } from "next/navigation";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const QualityAssistantButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/quality-assistant");

  return (
    <Link href={`/quality-assistant`}>
      <MenuButton
        label="Quality Assistant"
        isSelected={isSelected}
        iconName="assistant"
        type="open"
        color="primary"
      />
    </Link>
  );
};
