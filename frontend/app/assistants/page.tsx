"use client";
import { usePathname } from "next/navigation";
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

const Search = (): JSX.Element => {
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
          <div className={styles.message_wrapper}>
            <MessageInfoBox type="info">
              <span>
                Quivr assistants are AI-driven agents that apply specific
                processes to an input in order to generate a usable output.{" "}
                <br></br>This output can be directly uploaded to a digital brain
                or sent via email.{" "}
              </span>
            </MessageInfoBox>
          </div>
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

export default Search;
