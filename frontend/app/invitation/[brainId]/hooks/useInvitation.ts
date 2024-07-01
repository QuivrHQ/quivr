/* eslint-disable max-lines */
"use client";
import axios, { AxiosResponse } from "axios";
import { UUID } from "crypto";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { BrainRoleType } from "@/app/studio/[brainId]/BrainManagementTabs/components/PeopleTab/BrainUsers/types";
import { useSubscriptionApi } from "@/lib/api/subscription/useSubscriptionApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useOnboardingContext } from "@/lib/context/OnboardingProvider/hooks/useOnboardingContext";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/june/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useInvitation = () => {
  const { t } = useTranslation(["brain", "invitation"]);
  const params = useParams();
  const brainId = params?.brainId as UUID | undefined;
  const [isLoading, setIsLoading] = useState(false);
  const [brainName, setBrainName] = useState<string>("");
  const [role, setRole] = useState<BrainRoleType | undefined>();
  const [isProcessingRequest, setIsProcessingRequest] = useState(false);
  const { setIsBrainCreated } = useOnboardingContext();

  const { publish } = useToast();
  const { track } = useEventTracking();
  const { getInvitation, acceptInvitation, declineInvitation } =
    useSubscriptionApi();

  if (brainId === undefined) {
    throw new Error(t("brainUndefined", { ns: "brain" }));
  }

  const { fetchAllBrains, setCurrentBrainId } = useBrainContext();
  const router = useRouter();

  useEffect(() => {
    setIsLoading(true);

    const checkInvitationValidity = async () => {
      try {
        const { name, role: assignedRole } = await getInvitation(brainId);
        setBrainName(name);
        setRole(assignedRole);
      } catch (error) {
        if (axios.isAxiosError(error) && error.response?.status === 404) {
          publish({
            variant: "warning",
            text: t("invitationNotFound", { ns: "invitation" }),
          });
        } else {
          publish({
            variant: "danger",
            text: t("errorCheckingInvitation", { ns: "invitation" }),
          });
        }
        router.push("/");
      } finally {
        setIsLoading(false);
      }
    };
    void checkInvitationValidity();
  }, [brainId]);

  const handleAccept = async () => {
    setIsBrainCreated(true);
    setIsProcessingRequest(true);
    try {
      await acceptInvitation(brainId);
      void track("INVITATION_ACCEPTED");

      await fetchAllBrains();
      publish({
        variant: "success",
        text: t("accept", { ns: "invitation" }),
      });
      setCurrentBrainId(brainId);
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data !== undefined) {
        publish({
          variant: "danger",
          text: (
            error.response as AxiosResponse<{
              detail: string;
            }>
          ).data.detail,
        });
      } else {
        console.error("Error calling the API:", error);
        publish({
          variant: "danger",
          text: t("errorAccepting", { ns: "invitation" }),
        });
      }
    } finally {
      setIsProcessingRequest(false);
      void router.push("/chat");
    }
  };

  const handleDecline = async () => {
    setIsProcessingRequest(true);
    try {
      await declineInvitation(brainId);
      publish({
        variant: "success",
        text: t("declined", { ns: "invitation" }),
      });
      void track("INVITATION_DECLINED");
    } catch (error) {
      if (axios.isAxiosError(error) && error.response?.data !== undefined) {
        publish({
          variant: "danger",
          text: (
            error.response as AxiosResponse<{
              detail: string;
            }>
          ).data.detail,
        });
      } else {
        publish({
          variant: "danger",
          text: t("errorDeclining", { ns: "invitation" }),
        });
      }
    } finally {
      setIsProcessingRequest(false);
      void router.push("/chat");
    }
  };

  return {
    handleAccept,
    handleDecline,
    brainName,
    role,
    isLoading,
    isProcessingRequest,
  };
};
