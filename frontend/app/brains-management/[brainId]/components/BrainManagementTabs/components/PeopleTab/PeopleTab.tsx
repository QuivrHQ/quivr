/* eslint-disable max-lines */
"use client";

import { UUID } from "crypto";
import { useTranslation } from "react-i18next";
import { ImUserPlus } from "react-icons/im";
import { MdContentPaste, MdLink } from "react-icons/md";

import { BrainUsers } from "@/lib/components/BrainUsers/BrainUsers";
import { UserToInvite } from "@/lib/components/UserToInvite";
import Button from "@/lib/components/ui/Button";
import { useShareBrain } from "@/lib/hooks/useShareBrain";

type ShareBrainModalProps = {
  brainId: UUID;
};

export const PeopleTab = ({ brainId }: ShareBrainModalProps): JSX.Element => {
  const { t } = useTranslation(["translation","config","brain"]);
  const {
    roleAssignations,
    handleCopyInvitationLink,
    updateRoleAssignation,
    removeRoleAssignation,
    inviteUsers,
    addNewRoleAssignationRole,
    sendingInvitation,
    canAddNewRow,
    hasShareBrainRights,
  } = useShareBrain(brainId);

  if (!hasShareBrainRights) {
    return (
      <div className="flex justify-center items-center mt-5">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative max-w-md">
          <strong className="font-bold mr-1">{t("ohno",{ns:"config"})}</strong>
          <span className="block sm:inline">
            {t("roleRequired",{ns:"config"})}
          </span>
          <p>{t("requireAccess",{ns:"config"})}</p>
        </div>
      </div>
    );
  }

  return (
    <>
      <form
        onSubmit={(event) => {
          event.preventDefault();
          void inviteUsers();
        }}
      >
        <div>
          <div className="flex flex-row align-center my-5">
            <div
              onClick={() => void handleCopyInvitationLink()}
              className="cursor-pointer flex bg-gray-100 p-0 flex-1 flex-row border-gray-200 dark:border-gray-700 justify-space-between align-center rounded-md border-2"
            >
              <div className="px-8 py-3 text-sm disabled:opacity-80 text-center font-medium rounded-md focus:ring ring-primary/10 outline-none flex items-center justify-center gap-2 transition-opacity bg-transparent border-2 border-gray border-l-0 border-t-0 border-b-0 rounded-l-none">
                <MdLink size="20" color="gray" />
              </div>
              <div className="flex flex-row flex-1 items-center justify-center">
                <span className="text-sm text-gray-700 dark:text-gray-200 w-full bg-gray-50 dark:bg-gray-900 px-4 py-2">
                  {t("shareBrainLink",{ns:"brain"})}
                </span>
              </div>
              <Button type="button">
                <MdContentPaste />
              </Button>
            </div>
          </div>

          <div className="bg-gray-100 h-0.5 my-10 border-gray-200 dark:border-gray-700" />
          <p className="text-lg font-bold">{t("inviteUsers",{ns:"brain"})}</p>

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
            {t("shareButton",{ns:"translation"})}
          </Button>
        </div>
      </form>
      <div className="bg-gray-100 h-0.5 my-10 border-gray-200 dark:border-gray-700" />
      <p className="text-lg font-bold">{t("usersWithAccess",{ns:"brain"})}</p>
      <BrainUsers brainId={brainId} />
    </>
  );
};
