"use client";

import { useTranslation } from "react-i18next";

import Button from "@/lib/components/ui/Button";
import PageHeading from "@/lib/components/ui/PageHeading";
import Spinner from "@/lib/components/ui/Spinner";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { useInvitation } from "./hooks/useInvitation";

const InvitationPage = (): JSX.Element => {
  const { t } = useTranslation('invitation');
  const {
    handleAccept,
    isProcessingRequest,
    handleDecline,
    isLoading,
    brainName,
    role,
  } = useInvitation();
  const { session } = useSupabase();

  if (isLoading) {
    return <Spinner />;
  }

  if (session?.user === undefined) {
    redirectToLogin();
  }

  if (role === undefined) {
    // This should never happen
    // It is a way to prevent the page from crashing when invitation is invalid instead of throwing an error
    // The user will be redirected to the home page (handled in the useInvitation hook)
    return <div />;
  }

  return (
    <main className="pt-10">
      <PageHeading
        title={t("wellcome",{brain: brainName, ns: "invitation"})}
        subtitle={t("invitationMessage",{role: role, ns: "invitation"})}
      />
      {isProcessingRequest ? (
        <div className="flex flex-col items-center justify-center mt-5">
          <Spinner />
          <p className="text-center">{t("processingRequest",{ns: "invitation"})}</p>
        </div>
      ) : (
        <div className="flex flex-col items-center justify-center gap-5 mt-5">
          <Button
            onClick={() => void handleAccept()}
            variant={"secondary"}
            className="py-3"
          >
            {t("accept",{ns: "invitation"})}
          </Button>
          <Button
            onClick={() => void handleDecline()}
            variant={"danger"}
            className="py-3"
          >
            {t("reject",{ns: "invitation"})}
          </Button>
        </div>
      )}
    </main>
  );
};

export default InvitationPage;
