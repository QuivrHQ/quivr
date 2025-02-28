import Link from "next/link";
import { usePathname } from "next/navigation";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const AssistantsButton = (): JSX.Element => {
  const pathname = usePathname() ?? "";
  const isSelected = pathname.includes("/assistants");

  return (
    <Link href={`/assistants`}>
      <MenuButton
        label="Dobbie Assistants"
        isSelected={isSelected}
        iconName="assistant"
        type="open"
        color="primary"
      />
    </Link>
  );
};
