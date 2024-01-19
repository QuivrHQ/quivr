import { useTranslation } from "react-i18next";
import { LuPanelLeftClose, LuPanelRightClose } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";
import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";

export const MenuControlButton = (): JSX.Element => {
  const { isOpened, setIsOpened } = useMenuContext();
  const Icon = isOpened ? LuPanelLeftClose : LuPanelRightClose;
  const { t } = useTranslation("chat");

  return (
    <Button
      variant="tertiary"
      className="px-2 py-0"
      type="button"
      onClick={() => setIsOpened(!isOpened)}
    >
      <div className="flex flex-col items-center justify-center gap-1">
        <Icon className="text-2xl md:text-3xl self-center text-accent" />
        <span className="text-xs">{t("menu")}</span>
      </div>
    </Button>
  );
};
