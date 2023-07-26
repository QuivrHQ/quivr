import Link from "next/link";
import { FaBrain } from "react-icons/fa";
import { MdSettings } from "react-icons/md";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

export const BrainManagementButton = (): JSX.Element => {
  const { currentBrainId } = useBrainContext();

  return (
    <Link href={`/brains-management/${currentBrainId ?? ""}`}>
      <button type="button" className="flex items-center focus:outline-none">
        <MdSettings className="w-6 h-6" color="gray" />
        <FaBrain className="w-3 h-3" color="gray" />
      </button>
    </Link>
  );
};
