/* eslint-disable max-lines */
"use client";

import { UUID } from "crypto";
import { Fragment } from "react";
import { useTranslation } from "react-i18next";
import { ImUserPlus } from "react-icons/im";
import { MdContentPaste, MdShare } from "react-icons/md";

import { BrainUsers } from "@/lib/components/BrainUsers/BrainUsers";
import { UserToInvite } from "@/lib/components/UserToInvite";
import Button from "@/lib/components/ui/Button";
import { Modal } from "@/lib/components/ui/ModalPayment";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useShareBrain } from "@/lib/hooks/useShareBrain";

import { BrainRoleType } from "../BrainUsers/types";

type ShareBrainModalProps = {
  brainId: UUID;
};
const requiredAccessToShareBrain: BrainRoleType[] = ["Owner", "Editor"];

export const ShareBrain = ({ brainId }: ShareBrainModalProps): JSX.Element => {
  const {
    roleAssignations,
    brainShareLink,
    handleCopyInvitationLink,
    updateRoleAssignation,
    removeRoleAssignation,
    inviteUsers,
    addNewRoleAssignationRole,
    sendingInvitation,
    setIsShareModalOpen,
    isShareModalOpen,
    canAddNewRow,
  } = useShareBrain(brainId);

  const { t } = useTranslation(["translation", "brain"]);

  const { allBrains } = useBrainContext();
  const correspondingBrain = allBrains.find((brain) => brain.id === brainId);

  if (
    correspondingBrain === undefined ||
    !requiredAccessToShareBrain.includes(correspondingBrain.role)
  ) {
    return <Fragment />;
  }

  return (
    <Modal
      Trigger={
        <Button
          className="group-hover:visible invisible hover:text-red-500 transition-[colors,opacity] p-1"
          onClick={() => void 0}
          variant={"tertiary"}
          data-testId="share-brain-button"
        >
          <MdShare className="text-xl" />
        </Button>
      }
      CloseTrigger={<div />}
      title={t("shareBrain", { name: correspondingBrain.name, ns: "brain" })}
      isOpen={isShareModalOpen}
      setOpen={setIsShareModalOpen}
    >
      <form
        onSubmit={(event) => {
          event.preventDefault();
          void inviteUsers();
        }}
      >
        <div>
          <div className="flex flex-row align-center my-5">
            <div className="flex bg-gray-100 p-3 rounded flex-1 flex-row border-b border-gray-200 dark:border-gray-700 justify-space-between align-center">
              <div className="flex flex-1 overflow-hidden">
                <p className="flex-1 color-gray-500">{brainShareLink}</p>
              </div>
              <Button
                type="button"
                onClick={() => void handleCopyInvitationLink()}
              >
                <MdContentPaste />
              </Button>
            </div>
          </div>

          <div className="bg-gray-100 h-0.5 mb-5 border-gray-200 dark:border-gray-700" />

          {roleAssignations.map((roleAssignation, index) => (
            <UserToInvite
              key={roleAssignation.id}
              onChange={updateRoleAssignation(index)}
              removeCurrentInvitation={removeRoleAssignation(index)}
              roleAssignation={roleAssignation}
            />
          ))}
          <Button
            className="my-5"
            onClick={addNewRoleAssignationRole}
            disabled={sendingInvitation || !canAddNewRow}
            data-testid="add-new-row-role-button"
          >
            <ImUserPlus />
          </Button>
        </div>

        <div className="mb-3 flex flex-row justify-end">
          <Button
            isLoading={sendingInvitation}
            disabled={roleAssignations.length === 0}
            type="submit"
          >
            {t("shareButton")}
          </Button>
        </div>
      </form>
      <div className="bg-gray-100 h-0.5 mb-5 border-gray-200 dark:border-gray-700" />
      <p className="text-lg font-bold">
        {t("shareBrainUsers", { ns: "brain" })}
      </p>
      <BrainUsers brainId={brainId} />
    </Modal>
  );
};
