"use client";
import Link from "next/link";
import { MdSettings } from "react-icons/md";
import Button from "../../../../components/ui/Button";

export function ConfigButton() {
  return (
    <Link href={"/config"}>
      <Button className="px-3" variant={"tertiary"}>
        <MdSettings className="text-2xl" />
      </Button>
    </Link>
  );
}
