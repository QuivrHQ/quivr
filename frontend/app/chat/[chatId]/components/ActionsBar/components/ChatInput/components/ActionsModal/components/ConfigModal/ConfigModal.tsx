import { useTranslation } from "react-i18next";
import { LuChevronRight, LuSettings } from "react-icons/lu";
import { MdCheck } from "react-icons/md";

import { Modal } from "@/lib/components/ui/Modal";
import { defineMaxTokens } from "@/lib/helpers/defineMaxTokens";

import { useConfigModal } from "./hooks/useConfigModal";
import { Button } from "../Button";

export const ConfigModal = (): JSX.Element => {
  const {
    handleSubmit,
    isConfigModalOpen,
    setIsConfigModalOpen,
    register,
    maxTokens,
    model,
    accessibleModels,
  } = useConfigModal();
  const { t } = useTranslation(["config", "chat"]);

  return (
    <Modal
      Trigger={
        <Button
          label={t("chat:parameters")}
          startIcon={<LuSettings size={18} />}
          endIcon={<LuChevronRight size={18} />}
          className="w-full"
        />
      }
      title="Chat configuration"
      desc="Adjust your chat settings"
      isOpen={isConfigModalOpen}
      setOpen={setIsConfigModalOpen}
      CloseTrigger={<div />}
    >
      <form className="mt-10 flex flex-col items-center gap-2">
        <fieldset className="w-full flex flex-col">
          <label className="flex-1 text-sm" htmlFor="model">
            {t("modelLabel")}
          </label>
          <select
            {...register("model")}
            className="px-5 py-2 dark:bg-gray-700 bg-gray-200 rounded-md"
          >
            <option value="">{t("modelLabel")}</option>
            {accessibleModels.map((availableModel) => (
              <option value={availableModel} key={availableModel}>
                {availableModel}
              </option>
            ))}
          </select>
        </fieldset>
        <fieldset className="w-full flex mt-4">
          <label className="flex-1" htmlFor="tokens">
            Max tokens: {maxTokens}
          </label>
          <input
            type="range"
            min="10"
            max={defineMaxTokens(model)}
            value={maxTokens}
            {...register("maxTokens")}
          />
        </fieldset>

        <Button
          className="mt-12 self-end text-white"
          type="button"
          onClick={() => {
            handleSubmit();
            setIsConfigModalOpen(false);
          }}
          variant={"primary"}
          label="Save"
          endIcon={<MdCheck className="text-xl" />}
        />
      </form>
    </Modal>
  );
};
