/* eslint-disable max-lines */
"use client";
import { UUID } from "crypto";
import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { useSubscriptionApi } from "@/lib/api/subscription/useSubscriptionApi";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useToast } from "@/lib/hooks";

interface UseInvitationReturn {
  brainId: UUID | undefined;
  handleAccept: () => Promise<void>;
  handleDecline: () => Promise<void>;
  isValidInvitation: boolean;
  isLoading: boolean;
}

export const useInvitation = (): UseInvitationReturn => {
  const params = useParams();
  const brainId = params?.brainId as UUID | undefined;
  const { publish } = useToast();
  if (brainId === undefined) {
    throw new Error("Brain ID is undefined");
  }

  const [isLoading, setIsLoading] = useState(false);
  const [isValidInvitation, setIsValidInvitation] = useState(false);
  const { acceptInvitation, declineInvitation } = useSubscriptionApi();
  const checkValidInvitation = useCallback(
    useSubscriptionApi().checkValidInvitation,
    []
  );

  const { addBrain, setActiveBrain } = useBrainContext();
  const router = useRouter();
  // Check invitation on component mount
  useEffect(() => {
    setIsLoading(true);

    const checkInvitationValidity = async () => {
      try {
        console.log("Checking invitation validity...");
        const validInvitation = await checkValidInvitation(brainId);
        setIsValidInvitation(validInvitation);
        console.log("validInvitation", validInvitation);
        if (!validInvitation) {
          publish({
            variant: "warning",
            text: "This invitation is not valid.",
          });
          router.push("/");
        }
      } catch (error) {
        console.error("Error checking invitation validity:", error);
      } finally {
        setIsLoading(false);
      }
    };
    checkInvitationValidity().catch((error) => {
      console.error("Error checking invitation validity:", error);
    });
  }, [brainId, checkValidInvitation]);

  const handleAccept = async () => {
    // API call to accept the invitation
    // After success, redirect user to a specific page ->  chat page
    try {
      const response = await acceptInvitation(brainId);
      console.log(response.message);

      await addBrain(brainId);
      setActiveBrain({ id: brainId, name: "BrainName" });

      //set brainId as active brain
      publish({
        variant: "success",
        text: JSON.stringify(response.message),
      });
    } catch (error) {
      // @ts-ignore Error is of unknown type
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      if (error.response.data.detail !== undefined) {
        publish({
          variant: "danger",
          // @ts-ignore Error is of unknown type
          // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
          text: error.response.data.detail,
        });
      } else {
        console.error("Error calling the API:", error);
        publish({
          variant: "danger",
          text: "An unknown error occurred while accepting the invitaiton",
        });
      }
    } finally {
      void router.push("/chat");
    }
  };

  const handleDecline = async () => {
    // API call to accept the invitation
    // After success, redirect user to a specific page ->  home page
    try {
      const response = await declineInvitation(brainId);
      console.log(response.message);

      publish({
        variant: "success",
        text: JSON.stringify(response.message),
      });
    } catch (error) {
      // @ts-ignore Error is of unknown type
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      if (error.response.data.detail !== undefined) {
        publish({
          variant: "danger",
          // @ts-ignore Error is of unknown type
          // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
          text: error.response.data.detail,
        });
      } else {
        console.error("Error calling the API:", error);
        publish({
          variant: "danger",
          text: "An unknown error occurred while declining the invitaiton",
        });
      }
    } finally {
      void router.push("/upload");
    }
  };

  return {
    brainId,
    handleAccept,
    handleDecline,
    isValidInvitation,
    isLoading,
  };
};
