"use client";
import Button from "@/lib/components/ui/Button";
import Link from "next/link";
import { MdSettings } from "react-icons/md";

export function ConfigButton() {
  return (
    <Link href={"/config"}>
      <Button className="px-3" variant={"tertiary"}>
        <MdSettings className="text-2xl" />
      </Button>
    </Link>
  );
}
