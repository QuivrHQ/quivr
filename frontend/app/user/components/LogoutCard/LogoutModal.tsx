import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal";

import { useLogoutModal } from "./hooks/useLogoutModal";

export const LogoutModal = (): JSX.Element => {
  const { t } = useTranslation(["translation", "logout"]);
  const {
    handleLogout,
    isLoggingOut,
    isLogoutModalOpened,
    setIsLogoutModalOpened,
  } = useLogoutModal();

  return (
    <Modal
      Trigger={
        <Button className="px-3 py-2" variant="secondary">
          {t("logoutButton")}
        </Button>
      }
      isOpen={isLogoutModalOpened}
      setOpen={setIsLogoutModalOpened}
      CloseTrigger={<div />}
    >
      <div className="text-center flex flex-col items-center gap-5">
        <h2 className="text-lg font-medium mb-5">
          {t("areYouSure", { ns: "logout" })}
        </h2>
        <div className="flex gap-5 items-center justify-center">
          <Button
            onClick={() => setIsLogoutModalOpened(false)}
            variant={"primary"}
          >
            {t("cancel", { ns: "logout" })}
          </Button>
          <Button
            isLoading={isLoggingOut}
            variant={"danger"}
            onClick={() => void handleLogout()}
            data-testid="logout-button"
          >
            {t("logoutButton")}
          </Button>
        </div>
      </div>
    </Modal>
  );
};
