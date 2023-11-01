import { useTranslation } from "react-i18next";
import { MdAdd, MdLink } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal";
import { PublicBrain } from "@/lib/context/BrainProvider/types";

import { usePublicBrainItem } from "./hooks/usePublicBrainItem";
import { formatDate } from "./utils/formatDate";

type PublicBrainItemProps = {
  brain: PublicBrain;
};

export const PublicBrainItem = ({
  brain,
}: PublicBrainItemProps): JSX.Element => {
  const {
    handleSubscribeToBrain,
    isUserSubscribedToBrain,
    subscriptionRequestPending,
    isSubscriptionModalOpened,
    setIsSubscriptionModalOpened,
    handleCopyBrainLink,
  } = usePublicBrainItem({
    brainId: brain.id,
  });

  const { t } = useTranslation("brain");

  const subscribeButton = (
    <Button
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        void handleSubscribeToBrain();
      }}
      disabled={isUserSubscribedToBrain || subscriptionRequestPending}
      isLoading={subscriptionRequestPending}
      className="bg-primary text-white p-0 px-3 rounded-xl border-0 w-content mt-3"
    >
      {isUserSubscribedToBrain
        ? t("public_brain_already_subscribed_button_label")
        : t("public_brain_subscribe_button_label")}
      {!isUserSubscribedToBrain && <MdAdd className="text-md" />}
    </Button>
  );

  const isBrainDescriptionEmpty = brain.description === "";
  const brainDescription = isBrainDescriptionEmpty
    ? t("empty_brain_description")
    : brain.description;

  return (
    <Modal
      isOpen={isSubscriptionModalOpened}
      setOpen={setIsSubscriptionModalOpened}
      CloseTrigger={<div />}
      Trigger={
        <div className="flex p-5 justify-center items-center flex-col flex-1 w-full h-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden bg-white dark:bg-black border border-black/10 dark:border-white/25 md:p-5 cursor-pointer">
          <div>
            <p className="font-bold mb-5 text-xl line-clamp-1">{brain.name}</p>
          </div>
          <div className="flex-1">
            <p
              className={`line-clamp-1 text-center px-5 ${
                isBrainDescriptionEmpty && "text-gray-400"
              }`}
            >
              {brainDescription}
            </p>
          </div>
          {subscribeButton}
        </div>
      }
    >
      <div>
        <p className="text-2xl font-bold text-center mb-10">{brain.name}</p>
        <p className={`mb-10 ${isBrainDescriptionEmpty && "text-gray-400"}`}>
          {brainDescription}
        </p>
        <p className="font-bold mb-5">
          <span>
            <span className="mr-2">{t("public_brain_last_update_label")}:</span>
            {formatDate(brain.last_update)}
          </span>
        </p>
        <div className="flex flex-1 justify-between items-center">
          <Button
            onClick={() => void handleCopyBrainLink()}
            className="p-1 bg-white border-solid border border-gray-300 rounded-md hover:bg-gray-100"
          >
            <MdLink size="20" color="gray" />
          </Button>
          {subscribeButton}
        </div>
      </div>
    </Modal>
  );
};
