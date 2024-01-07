import Link from "next/link";
import { useTranslation } from "react-i18next";
import { LuChevronRight, LuMessageSquarePlus } from "react-icons/lu";

import { Button } from "./Button";

export const NewDiscussionButton = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);

  return (
    <Link href="/chat">
      <Button
        label={t("new_discussion")}
        startIcon={<LuMessageSquarePlus size={18} />}
        endIcon={<LuChevronRight size={18} />}
        className="w-full"
      />
    </Link>
  );
};
