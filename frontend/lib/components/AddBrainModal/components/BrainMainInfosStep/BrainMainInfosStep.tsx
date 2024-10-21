import { useState } from "react";

import { BrainSnippet } from "@/lib/components/BrainSnippet/BrainSnippet";
import { FieldHeader } from "@/lib/components/ui/FieldHeader/FieldHeader";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { TextAreaInput } from "@/lib/components/ui/TextAreaInput/TextAreaInput";
import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

import styles from "./BrainMainInfosStep.module.scss";

import { useBrainCreationContext } from "../../brainCreation-provider";

export const BrainMainInfosStep = (): JSX.Element => {
  const [editSnippet, setEditSnippet] = useState<boolean>(false);
  const [name, setName] = useState<string>("");
  const [description, setDescription] = useState<string>("");
  const [instructions, setInstructions] = useState<string>("");
  const { snippetColor, setSnippetColor, snippetEmoji, setSnippetEmoji } =
    useBrainCreationContext();

  // const feed = async (): Promise<void> => {
  //   if (!userIdentityData?.onboarded) {
  //     await updateUserIdentity({
  //       ...userIdentityData,
  //       username: userIdentityData?.username ?? "",
  //       onboarded: true,
  //     });
  //   }
  //   setCreating(true);
  //   createBrain();
  // };

  return (
    <div className={styles.brain_main_infos_container}>
      <div className={styles.brain_main_infos_wrapper}>
        <div className={styles.inputs_wrapper}>
          <span className={styles.title}>Define brain identity</span>
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
          <div>
            <FieldHeader
              iconName="paragraph"
              label="Description"
              mandatory={true}
            />

            <TextAreaInput
              label="Enter your brain description"
              inputValue={description}
              setInputValue={setDescription}
            />
          </div>
          <div>
            <FieldHeader
              iconName="paragraph"
              label="Description"
              mandatory={true}
            />

            <TextAreaInput
              label="Enter your brain description"
              inputValue={instructions}
              setInputValue={setInstructions}
            />
          </div>
        </div>
        <div className={styles.buttons_wrapper}>
          <QuivrButton
            color="primary"
            label="Create"
            onClick={() => console.info("hey")}
            iconName="chevronRight"
            important={true}
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
