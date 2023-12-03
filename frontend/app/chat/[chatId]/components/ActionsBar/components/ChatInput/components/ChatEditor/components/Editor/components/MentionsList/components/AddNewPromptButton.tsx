import { useRouter } from "next/navigation";
import { useTranslation } from "react-i18next";
import { MdAdd } from "react-icons/md";

import Button from "@/lib/components/ui/Button";

export const AddNewPromptButton = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);
  const router = useRouter();

  return (
    <Button
      onClick={() => router.push("/brains-management")}
      variant={"tertiary"}
      className={"border-0"}
      data-testid="add-brain-button"
    >
      {t("new_prompt")}
      <MdAdd className="text-xl" />
    </Button>
  );
};
