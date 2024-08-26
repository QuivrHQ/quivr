"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";

export const NoteButton = (): JSX.Element => {
  const pathname = usePathname();
  const isSelected = pathname ? pathname.includes("/note") : false;

  return (
    <Link href={`/note`}>
      <MenuButton
        label="My Notebook"
        isSelected={isSelected}
        iconName="note"
        type="open"
        color="primary"
      />
    </Link>
  );
};
