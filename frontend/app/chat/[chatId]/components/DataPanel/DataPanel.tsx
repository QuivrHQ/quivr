"use client";

import { useEffect, useState } from "react";

import { FoldableSection } from "@/lib/components/ui/FoldableSection/FoldableSection";
import { useChatContext } from "@/lib/context";
import { Source } from "@/lib/types/MessageMetadata";

import styles from "./DataPanel.module.scss";

import { ChatMessage } from "../../types";

const DataPanel = (): JSX.Element => {
  const { messages } = useChatContext();
  const [selectedMessageSources, setSelectedMessageSources] =
    useState<Source[]>();
  const { sourcesMessageIndex } = useChatContext();

  useEffect(() => {
    console.info(sourcesMessageIndex);
    if (messages.length > 0 && sourcesMessageIndex !== undefined) {
      const selectedMessage: ChatMessage = messages[sourcesMessageIndex];
      const newSources: Source[] = (
        selectedMessage.metadata?.sources ?? []
      ).map((source: Source) => ({
        ...source,
        frequency: 0,
      }));

      const updatedSources: Source[] = [];

      newSources.forEach((newSource) => {
        const existingSourceIndex = updatedSources.findIndex(
          (source) => source.name.trim() === newSource.name.trim()
        );
        if (existingSourceIndex !== -1) {
          updatedSources[existingSourceIndex] = {
            ...updatedSources[existingSourceIndex],
            frequency: updatedSources[existingSourceIndex].frequency + 1,
          };
        } else {
          updatedSources.push(newSource);
        }
      });

      updatedSources.sort((a, b) => b.frequency - a.frequency);

      setSelectedMessageSources(updatedSources);
    }
  }, [messages, sourcesMessageIndex]);

  return (
    <div className={styles.data_panel_wrapper}>
      <FoldableSection
        label="Sources"
        icon="file"
        foldedByDefault={selectedMessageSources?.length === 0}
      >
        <div className={styles.sources_wrapper}>
          {selectedMessageSources?.map((source, index) => (
            <div className={styles.source_wrapper} key={index}>
              <a
                href={source.source_url}
                key={index}
                target="_blank"
                rel="noopener noreferrer"
              >
                <div className={styles.source}>{source.name}</div>
              </a>
            </div>
          ))}
        </div>
      </FoldableSection>
    </div>
  );
};

export default DataPanel;
