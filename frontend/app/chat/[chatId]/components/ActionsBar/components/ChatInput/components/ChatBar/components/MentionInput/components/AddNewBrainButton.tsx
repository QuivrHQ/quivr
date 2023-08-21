import Link from "next/link";

import Button from "@/lib/components/ui/Button";

export const AddNewBrainButton = (): JSX.Element => (
  <Link
    href={"/brains-management"}
    onClick={(event) => {
      event.preventDefault();
      event.stopPropagation();
    }}
  >
    <Button variant={"tertiary"}>Add new brain</Button>
  </Link>
);
