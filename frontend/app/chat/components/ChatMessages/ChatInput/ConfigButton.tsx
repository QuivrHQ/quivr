"use client";
import Link from "next/link";
import { MdSettings } from "react-icons/md";

import Button from "@/lib/components/ui/Button";

export const ConfigButton = (): JSX.Element => {
  return (
    <Link href={"/config"}>
      <Button className="p-2 sm:px-3" variant={"tertiary"}>
        <MdSettings className="text-lg sm:text-xl lg:text-2xl" />
      </Button>
    </Link>
  );
};
