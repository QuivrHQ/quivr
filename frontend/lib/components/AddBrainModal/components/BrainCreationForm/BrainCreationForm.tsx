import { useState } from "react";

import { BrainSnippet } from "@/lib/components/BrainSnippet/BrainSnippet";
import { FieldHeader } from "@/lib/components/ui/FieldHeader/FieldHeader";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextAreaInput } from "@/lib/components/ui/TextAreaInput/TextAreaInput";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./BrainCreationForm.module.scss";

import { useBrainCreationContext } from "../../brainCreation-provider";
import { useBrainCreationApi } from "../hooks/useBrainCreationApi";

export const BrainCreationForm = (): JSX.Element => {
  const [editSnippet, setEditSnippet] = useState<boolean>(false);
  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [instructions, setInstructions] = useState<string>("");
  const { snippetColor, setSnippetColor, snippetEmoji, setSnippetEmoji } =
    useBrainCreationContext();
  const { setCreating, creating } = useBrainCreationContext();
  const { createBrain } = useBrainCreationApi();

  const feed = (): void => {
    setCreating(true);
    createBrain({ name, description });
  };

  return (
    <div className={styles.brain_main_infos_container}>
      <div className={styles.brain_main_infos_wrapper}>
        <div className={styles.inputs_wrapper}>
          <div className={styles.first_line_wrapper}>
            <div className={styles.name_field}>
              <FieldHeader iconName="brain" label="Name" mandatory={true} />
              <TextInput
                label="Enter your brain name"
                inputValue={name}
                setInputValue={setName}
              />
            </div>
            <div className={styles.brain_snippet_wrapper}>
              <div
                className={styles.brain_snippet}
                style={{ backgroundColor: snippetColor }}
                onClick={() => {
                  if (!editSnippet) {
                    setEditSnippet(true);
                  }
                }}
              >
                <span>{snippetEmoji}</span>
              </div>
              <QuivrButton
                label="Edit"
                iconName="edit"
                color="primary"
                onClick={() => setEditSnippet(true)}
                small={true}
              />
            </div>
          </div>
          <div className={styles.text_areas_wrapper}>
            <div>
              <FieldHeader
                iconName="paragraph"
                label="Instructions"
                help="The instructions guide the Brain to generate a response tailored to your needs. It tells the AI what task to perform, what format to follow, and any specific details to consider. Clear, detailed instructions help the AI provide more accurate, relevant, and helpful responses."
              />

              <TextAreaInput
                label="Enter your brain instructions"
                inputValue={instructions}
                setInputValue={setInstructions}
              />
            </div>
            <div>
              <FieldHeader
                iconName="paragraph"
                label="Description"
                help="The description helps you easily identify the purpose of your brain. It provides a quick summary of what the brain is designed to do, making it easier to manage and distinguish from others. This field is for your reference and has no effect on how the AI performs tasks."
              />

              <TextAreaInput
                label="Enter your brain description"
                inputValue={description}
                setInputValue={setDescription}
              />
            </div>
          </div>
        </div>
        <div className={styles.buttons_wrapper}>
          <QuivrButton
            color="primary"
            label="Create"
            onClick={() => feed()}
            iconName="chevronRight"
            important={true}
            disabled={!name || !description || !instructions}
            isLoading={creating}
          />
        </div>
      </div>
      {editSnippet && (
        <div className={styles.edit_snippet}>
          <BrainSnippet
            setVisible={setEditSnippet}
            initialColor={snippetColor}
            initialEmoji={snippetEmoji}
            onSave={(color: string, emoji: string) => {
              setSnippetColor(color);
              setSnippetEmoji(emoji);
            }}
          />
        </div>
      )}
    </div>
  );
};
