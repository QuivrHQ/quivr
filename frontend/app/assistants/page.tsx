"use client";
import { redirect, usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { Assistant } from "@/lib/api/assistants/types";
import { useAssistants } from "@/lib/api/assistants/useAssistants";
import PageHeader from "@/lib/components/PageHeader/PageHeader";
import { BrainCard } from "@/lib/components/ui/BrainCard/BrainCard";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { AssistantModal } from "./AssistantModal/AssistantModal";
import styles from "./page.module.scss";

const Assistants = (): JSX.Element => {
  const pathname = usePathname();
  const { session } = useSupabase();
  const [assistants, setAssistants] = useState<Assistant[]>([]);
  const [assistantModalOpened, setAssistantModalOpened] =
    useState<boolean>(false);
  const [currentAssistant, setCurrentAssistant] = useState<Assistant | null>(
    null
  );

  const { getAssistants } = useAssistants();

  useEffect(() => {
    // REMOVE FOR NOW ACCESS TO QUIVR ASSISTANTS
    redirect("/search");
    if (session === null) {
      redirectToLogin();
    }

    void (async () => {
      try {
        const res = await getAssistants();
        if (res) {
          setAssistants(res);
        }
      } catch (error) {
        console.error(error);
      }
    })();
  }, [pathname, session]);

  return (
    <>
      <div className={styles.page_header}>
        <PageHeader
          iconName="assistant"
          label="Quivr Assistants"
          buttons={[]}
        />
        <div className={styles.content_wrapper}>
          <MessageInfoBox type="info">
            <div className={styles.message_wrapper}>
              <span>
                A Quivr Assistant is an AI agent that apply specific processes
                to an input in order to generate a usable output.
              </span>
              <span>
                For now, you can try the summary assistant, that summarizes a
                document and send the result by email or upload it in one of
                your brains.
              </span>
              <span> But don&apos;t worry! Other assistants are cooking!</span>
            </div>
          </MessageInfoBox>
          <MessageInfoBox type="warning">
            <div className={styles.message_wrapper}>
              <span>
                <strong>Feature still in Beta.</strong> Please provide feedbacks
                on the chat below!
              </span>
            </div>
          </MessageInfoBox>
          <div className={styles.assistants_grid}>
            {assistants.map((assistant) => {
              return (
                <BrainCard
                  tooltip={assistant.description}
                  brainName={assistant.name}
                  tags={assistant.tags}
                  imageUrl={assistant.icon_url}
                  callback={() => {
                    setAssistantModalOpened(true);
                    setCurrentAssistant(assistant);
                  }}
                  key={assistant.name}
                  cardKey={assistant.name}
                />
              );
            })}
          </div>
        </div>
      </div>
      {currentAssistant && (
        <AssistantModal
          isOpen={assistantModalOpened}
          setIsOpen={setAssistantModalOpened}
          assistant={currentAssistant}
        />
      )}
    </>
  );
};

export default Assistants;
