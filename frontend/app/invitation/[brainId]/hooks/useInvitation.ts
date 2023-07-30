/* eslint-disable max-lines */
"use client";
import axios, { AxiosResponse } from "axios";
import { UUID } from "crypto";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { useSubscriptionApi } from "@/lib/api/subscription/useSubscriptionApi";
import { BrainRoleType } from "@/lib/components/NavBar/components/NavItems/components/BrainsDropDown/components/BrainActions/types";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useToast } from "@/lib/hooks";
import { useEventTracking } from "@/services/analytics/useEventTracking";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useInvitation = () => {
  const params = useParams();
  const brainId = params?.brainId as UUID | undefined;
  const [isLoading, setIsLoading] = useState(false);
  const [brainName, setBrainName] = useState<string>("");
  const [role, setRole] = useState<BrainRoleType | undefined>();
  const [isProcessingRequest, setIsProcessingRequest] = useState(false);

  const { publish } = useToast();
  const { track } = useEventTracking();
  const { getInvitation, acceptInvitation, declineInvitation } =
    useSubscriptionApi();

  if (brainId === undefined) {
    throw new Error("Brain ID is undefined");
  }

  const { fetchAllBrains, setActiveBrain } = useBrainContext();
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
            text: "This invitation is not valid.",
          });
        } else {
          publish({
            variant: "danger",
            text: "An unknown error occurred while checking the invitaiton",
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
    setIsProcessingRequest(true);
    try {
      const response = await acceptInvitation(brainId);
      void track("INVITATION_ACCEPTED");

      await fetchAllBrains();
      publish({
        variant: "success",
        text: JSON.stringify(response.message),
      });
      setActiveBrain({ id: brainId, name: brainName });
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
          text: "An unknown error occurred while accepting the invitaiton",
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
      const response = await declineInvitation(brainId);
      publish({
        variant: "success",
        text: JSON.stringify(response.message),
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
          text: "An unknown error occurred while declining the invitation",
        });
      }
    } finally {
      setIsProcessingRequest(false);
      void router.push("/upload");
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
