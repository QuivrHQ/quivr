import Link from "next/link";

import Button from "@/lib/components/ui/Button";
import { useTranslation } from "react-i18next";

export const AddNewBrainButton = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);

  return (
    <Link
      href={"/brains-management"}
      onClick={(event) => {
        event.preventDefault();
        event.stopPropagation();
      }}
    >
      <Button className="px-5 py-2 text-sm" variant={"tertiary"}>
        {t("new_brain")}
      </Button>
    </Link>
  );
};
