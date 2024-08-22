import { useTranslation } from "react-i18next";
import { SiMicrosoftazure } from "react-icons/si";

import Button from "@/lib/components/ui/Button";

import { useAzureLogin } from "./hooks/useAzureLogin";

export const AzureLoginButton = (): JSX.Element => {
  const { isPending, signInWithAzure } = useAzureLogin();
  const { t } = useTranslation(["login"]);

  return (
    <Button
      onClick={() => void signInWithAzure()}
      isLoading={isPending}
      type="button"
      data-testid="azure-login-button"
      className="font-normal bg-white text-black py-2 hover:text-white"
    >
      <SiMicrosoftazure />
      {t("azureLogin", { ns: "login" })}
    </Button>
  );
};
