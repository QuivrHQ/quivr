import Link from "next/link";
import { useTranslation } from "react-i18next";
import { MdAdd } from "react-icons/md";

export const AddNewPromptButton = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);

  return (
    <Link
      href={"/brains-management"}
      className="flex px-5 py-3 text-sm decoration-none text-center w-full justify-between items-center"
    >
      {t("new_prompt")}
      <MdAdd />
    </Link>
  );
};
