import Link from "next/link";
import { MdSettings } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

export const BrainManagementButton = (): JSX.Element => {
  const { currentBrainId } = useBrainContext();

  return (
    <Link href={`/brains-management/${currentBrainId ?? ""}`}>
      <Button
        variant={"tertiary"}
        className="focus:outline-none text-2xl"
        aria-label="Settings"
      >
        <MdSettings />
      </Button>
    </Link>
  );
};
