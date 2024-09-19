"use client";

import { useEffect, useState } from "react";

import { useAssistants } from "@/lib/api/assistants/useAssistants";
import { Checkbox } from "@/lib/components/ui/Checkbox/Checkbox";
import { FileInput } from "@/lib/components/ui/FileInput/FileInput";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";
import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";

import AssistantCard from "./AssistantCard/AssistantCard";
import styles from "./AssistantTab.module.scss";


import { Assistant } from "../types/assistant";

const AssistantTab = (): JSX.Element => {
  const [assistantChoosed, setAssistantChoosed] = useState<
    Assistant | undefined
  >(undefined);
  const [assistants, setAssistants] = useState<Assistant[]>([]);
  const [booleanStates, setBooleanStates] = useState<{
    [key: string]: boolean;
  }>({});
  const [selectTextStates, setSelectTextStates] = useState<{
    [key: string]: string;
  }>({});

  const { getAssistants } = useAssistants();

  const handleFileChange = (file: File) => {
    console.log("Selected file:", file);
  };

  useEffect(() => {
    void (async () => {
      try {
        const res = await getAssistants();
        setAssistants(res);
      } catch (error) {
        console.error(error);
      }
    })();
  }, [assistantChoosed]);

  useEffect(() => {
    if (assistantChoosed && assistantChoosed.inputs.booleans) {
      const initialBooleanStates = assistantChoosed.inputs.booleans.reduce(
        (acc, input) => ({ ...acc, [input.key]: false }),
        {}
      );
      setBooleanStates(initialBooleanStates);
    }
    if (assistantChoosed && assistantChoosed.inputs.select_texts) {
      const initialSelectTextStates =
        assistantChoosed.inputs.select_texts.reduce(
          (acc, input) => ({ ...acc, [input.key]: input.default }),
          {}
        );
      setSelectTextStates(initialSelectTextStates);
    }
  }, [assistantChoosed]);

  const handleCheckboxChange = (key: string, checked: boolean) => {
    setBooleanStates((prevState) => ({
      ...prevState,
      [key]: checked,
    }));
  };

  return (
    <div className={styles.assistant_tab_wrapper}>
      {!assistantChoosed ? (
        <div className={styles.content_section}>
          <span className={styles.title}>Choose an assistant</span>
          <div className={styles.assistant_choice_wrapper}>
            {assistants.map((assistant, index) => (
              <div key={index} onClick={() => setAssistantChoosed(assistant)}>
                <AssistantCard assistant={assistant} />
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className={styles.form_wrapper}>
          <span className={styles.title}>{assistantChoosed.name}</span>
          <div className={styles.file_inputs_wrapper}>
            {assistantChoosed.inputs.files.map((input, index) => (
              <div className={styles.file_input_wrapper} key={index}>
                <div className={styles.file_header}>
                  <Icon name="file" color="black" size="small" />
                  <span>{input.key}</span>
                </div>
                <FileInput label={input.key} onFileChange={handleFileChange} />
              </div>
            ))}
          </div>
          {assistantChoosed.inputs.select_texts && (
            <div className={styles.select_texts_wrapper}>
              {assistantChoosed.inputs.select_texts.map((input, index) => (
                <div key={index} className={styles.select_text}>
                  <SingleSelector
                    iconName="brain"
                    placeholder={input.key}
                    options={input.options.map((option) => {
                      return { label: option, value: option };
                    })}
                    onChange={(value) =>
                      setSelectTextStates((prevState) => ({
                        ...prevState,
                        [input.key]: value,
                      }))
                    }
                    selectedOption={{
                      label: input.options[0],
                      value: input.options[0],
                    }}
                  />
                </div>
              ))}
            </div>
          )}
          {assistantChoosed.inputs.booleans && (
            <div className={styles.boolean_inputs_wrapper}>
              {assistantChoosed.inputs.booleans.map((input, index) => (
                <div key={index} className={styles.boolean_input}>
                  <Checkbox
                    label={input.key}
                    checked={booleanStates[input.key]}
                    setChecked={(checked) =>
                      handleCheckboxChange(input.key, checked)
                    }
                  />
                </div>
              ))}
            </div>
          )}
        </div>
      )}
      {assistantChoosed && (
        <div className={styles.buttons_wrapper}>
          <QuivrButton
            iconName="chevronLeft"
            label="Back"
            color="primary"
            onClick={() => setAssistantChoosed(undefined)}
          />
          <QuivrButton
            iconName="chevronRight"
            label="EXECUTE"
            color="primary"
            important={true}
          />
        </div>
      )}
    </div>
  );
};

export default AssistantTab;
