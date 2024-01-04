import { useTranslation } from "react-i18next";
import { CgFileDocument } from "react-icons/cg";
import { LuPlusCircle } from "react-icons/lu";
import { MdLink } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/Modal";
import { PublicBrain } from "@/lib/context/BrainProvider/types";
import { getBrainIconFromBrainType } from "@/lib/helpers/getBrainIconFromBrainType";

import { SecretsDefinitionFields } from "./components/SecretsDefinitionFields";
import { usePublicBrainItem } from "./hooks/usePublicBrainItem";
import { formatDate } from "./utils/formatDate";

type PublicBrainItemProps = {
  brain: PublicBrain;
};

export const PublicBrainItem = ({
  brain,
}: PublicBrainItemProps): JSX.Element => {
  const {
    isUserSubscribedToBrain,
    subscriptionRequestPending,
    isSubscriptionModalOpened,
    setIsSubscriptionModalOpened,
    handleCopyBrainLink,
    handleBrainSubscription,
    register,
  } = usePublicBrainItem({
    brain,
  });

  const { t } = useTranslation("brain");

  const subscribeButton = (
    <Button
      onClick={(e) => {
        e.preventDefault();
        e.stopPropagation();
        void handleBrainSubscription();
      }}
      disabled={isUserSubscribedToBrain || subscriptionRequestPending}
      isLoading={subscriptionRequestPending}
      className="bg-secondary text-primary rounded-lg border-0 w-content mt-3 disabled:bg-secondary hover:bg-primary/50 disabled:hover:bg-primary/50 w-full text-md"
    >
      {!isUserSubscribedToBrain && <LuPlusCircle className="text-md" />}
      {isUserSubscribedToBrain
        ? t("public_brain_already_subscribed_button_label")
        : t("public_brain_subscribe_button_label")}
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
        <div className="flex justify-center items-center flex-col flex-1 w-full h-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl overflow-hidden bg-white dark:bg-black border border-black/10 dark:border-white/25 cursor-pointer pb-2">
          <div className="w-full">
            <div className="w-full py-2 flex gap-2 justify-center items-center bg-primary bg-opacity-40 px-2">
              {getBrainIconFromBrainType(brain.brain_type, {
                iconSize: 24,
                DocBrainIcon: CgFileDocument,
                iconClassName: "text-primary",
              })}
              <span className="line-clamp-1 mr-2 font-semibold text-md">
                {brain.name}
              </span>
            </div>
          </div>
          <div className="flex-1 py-2">
            <p
              className={`line-clamp-2 text-center px-5 ${
                isBrainDescriptionEmpty && "text-gray-400"
              }`}
            >
              {brainDescription}
            </p>
          </div>
          <div className="w-full px-2">{subscribeButton}</div>
        </div>
      }
    >
      <div>
        <p className="text-2xl font-medium text-center mb-10 flex items-center justify-center">
          <span className="mr-2">
            {getBrainIconFromBrainType(brain.brain_type, {
              iconSize: 30,
              DocBrainIcon: CgFileDocument,
            })}
          </span>
          {brain.name}
        </p>
        <p className={`mb-10 ${isBrainDescriptionEmpty && "text-gray-400"}`}>
          {brainDescription}
        </p>
        <p className="mb-5">
          <span>
            <span className="mr-2">{t("public_brain_last_update_label")}:</span>
            {formatDate(brain.last_update)}
          </span>
        </p>
        <SecretsDefinitionFields
          register={register}
          secrets={brain.brain_definition?.secrets}
        />
        <div className="flex flex-1 justify-between items-center">
          <Button
            onClick={() => void handleCopyBrainLink()}
            className="p-1 bg-white border-solid border border-gray-300 rounded-md hover:bg-gray-100"
          >
            <MdLink size="20" color="gray" />
          </Button>
          <div>{subscribeButton}</div>
        </div>
      </div>
    </Modal>
  );
};
