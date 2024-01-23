import { UUID } from "crypto";
import { Fragment } from "react";
import { useTranslation } from "react-i18next";

import { useBrainFetcher } from "@/app/brains-management/[brainId]/components/BrainManagementTabs/hooks/useBrainFetcher";

import { useApiBrainSecretsInputs } from "./hooks/useApiBrainSecretsInputs";

import Button from "../ui/Button";

type ApiBrainSecretsInputsProps = {
  brainId: UUID;
  onUpdate?: () => void;
};

export const ApiBrainSecretsInputs = ({
  brainId,
  onUpdate,
}: ApiBrainSecretsInputsProps): JSX.Element => {
  const { brain } = useBrainFetcher({
    brainId,
  });
  const { register, updateSecrets, isPending, isUpdateButtonDisabled } =
    useApiBrainSecretsInputs({
      brainId,
      onUpdate,
    });
  const { t } = useTranslation(["brain"]);

  const secrets = brain?.brain_definition?.secrets;

  if (secrets === undefined || secrets.length === 0) {
    return <Fragment />;
  }

  return (
    <form
      onSubmit={(ev) => {
        ev.preventDefault();
        void updateSecrets();
      }}
    >
      <div className="mb-3">
        <p className="text-center mt-3">{t("update_secrets_message")}</p>
        <div className="grid md:grid-cols-3 gap-3">
          {secrets.map((secret) => (
            <div key={secret.name} className="flex flex-col">
              <div className="flex flex-col">
                <p className="text-sm font-bold mb-1">{secret.name}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {secret.description}
                </p>
              </div>
              <div className="flex flex-col">
                <input
                  type="text"
                  className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder={secret.description}
                  {...register(secret.name)}
                />
              </div>
            </div>
          ))}
        </div>
        <div className="mt-4 flex justify-end">
          <Button disabled={isUpdateButtonDisabled} isLoading={isPending}>
            {t("update_secrets_button")}
          </Button>
        </div>
      </div>
    </form>
  );
};
