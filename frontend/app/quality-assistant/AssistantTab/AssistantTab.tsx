"use client";

import { useEffect, useState } from "react";

import { useAssistants } from "@/lib/api/assistants/useAssistants";
import { FileInput } from "@/lib/components/ui/FileInput/FileInput";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import AssistantCard from "./AssistantCard/AssistantCard";
import styles from "./AssistantTab.module.scss";
import BooleansInputs from "./BooleansInputs/BooleansInputs";
import SelectorsInputs from "./SelectorsInput/SelectorsInputs";

import { Assistant, ProcessAssistantData } from "../types/assistant";

export interface ProcessAssistantInput {
  input: ProcessAssistantData;
  files: File[];
}

interface AssistantTabProps {
  setSelectedTab: (tab: string) => void;
}

const FILE_TYPES = ["pdf", "docx", "doc", "txt", "xlsx", "xls"];

const useAssistantData = () => {
  const [assistants, setAssistants] = useState<Assistant[]>([]);
  const [assistantChoosed, setAssistantChoosed] = useState<
    Assistant | undefined
  >(undefined);
  const { getAssistants } = useAssistants();

  useEffect(() => {
    void (async () => {
      try {
        const res = await getAssistants();
        setAssistants(res);
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  return { assistants, assistantChoosed, setAssistantChoosed };
};

const useFormStates = (assistantChoosed: Assistant | undefined) => {
  const [booleanStates, setBooleanStates] = useState<{
    [key: string]: boolean | null;
  }>({});
  const [selectTextStates, setSelectTextStates] = useState<{
    [key: string]: string | null;
  }>({});
  const [fileStates, setFileStates] = useState<{ [key: string]: File }>({});
  const [isFormValid, setIsFormValid] = useState<boolean>(false);

  useEffect(() => {
    if (assistantChoosed?.inputs.booleans) {
      const initialBooleanStates = assistantChoosed.inputs.booleans.reduce(
        (acc, input) => ({ ...acc, [input.key]: false }),
        {}
      );
      setBooleanStates(initialBooleanStates);
    }
    if (assistantChoosed?.inputs.select_texts) {
      const initialSelectTextStates =
        assistantChoosed.inputs.select_texts.reduce(
          (acc, input) => ({ ...acc, [input.key]: input.options[0] }),
          {}
        );
      setSelectTextStates(initialSelectTextStates);
    }
  }, [assistantChoosed]);

  return {
    booleanStates,
    setBooleanStates,
    selectTextStates,
    setSelectTextStates,
    fileStates,
    setFileStates,
    isFormValid,
    setIsFormValid,
  };
};

const validateForm = (
  assistantChoosed: Assistant | undefined,
  booleanStates: { [x: string]: boolean | null },
  fileStates: { [x: string]: File | undefined },
  selectTextStates: { [x: string]: string | null }
) => {
  if (!assistantChoosed) {
    return false;
  }

  const allBooleansSet =
    assistantChoosed.inputs.booleans?.every(
      (input) =>
        booleanStates[input.key] !== undefined &&
        booleanStates[input.key] !== null
    ) ?? true;

  const allFilesSet = assistantChoosed.inputs.files.every(
    (input) => fileStates[input.key] !== undefined
  );

  const allSelectTextsSet =
    assistantChoosed.inputs.select_texts?.every(
      (input) =>
        selectTextStates[input.key] !== undefined &&
        selectTextStates[input.key] !== null
    ) ?? true;

  return allBooleansSet && allFilesSet && allSelectTextsSet;
};

const AssistantTab = ({ setSelectedTab }: AssistantTabProps): JSX.Element => {
  const { assistants, assistantChoosed, setAssistantChoosed } =
    useAssistantData();
  const {
    booleanStates,
    setBooleanStates,
    selectTextStates,
    setSelectTextStates,
    fileStates,
    setFileStates,
    isFormValid,
    setIsFormValid,
  } = useFormStates(assistantChoosed);
  const { processTask } = useAssistants();
  const [loading, setLoading] = useState<boolean>(false);

  const handleFileChange = (key: string, file: File) => {
    setFileStates((prevState) => ({
      ...prevState,
      [key]: file,
    }));
  };

  useEffect(() => {
    setIsFormValid(
      validateForm(
        assistantChoosed,
        booleanStates,
        fileStates,
        selectTextStates
      )
    );
  }, [booleanStates, fileStates, selectTextStates, assistantChoosed]);

  const handleSubmit = async () => {
    if (assistantChoosed) {
      const processAssistantData: ProcessAssistantData = {
        id: assistantChoosed.id,
        name: assistantChoosed.name,
        inputs: {
          files: Object.keys(fileStates).map((key) => ({
            key,
            value: fileStates[key].name,
          })),
          booleans: Object.keys(booleanStates).map((key) => ({
            key,
            value: booleanStates[key] ?? null,
          })),
          select_texts: Object.keys(selectTextStates).map((key) => ({
            key,
            value: selectTextStates[key],
          })),
        },
      };

      const processAssistantInput: ProcessAssistantInput = {
        input: processAssistantData,
        files: Object.values(fileStates),
      };

      setLoading(true);
      await processTask(processAssistantInput);
      setSelectedTab("Process");
      setLoading(false);
    }
  };

  const resetForm = () => {
    setBooleanStates({});
    setSelectTextStates({});
    setFileStates({});
    setIsFormValid(false);
  };

  const handleBack = () => {
    resetForm();
    setAssistantChoosed(undefined);
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
                <FileInput
                  label={input.key}
                  onFileChange={(file) => handleFileChange(input.key, file)}
                  acceptedFileTypes={FILE_TYPES}
                />
              </div>
            ))}
          </div>
          <SelectorsInputs
            selectTexts={assistantChoosed.inputs.select_texts ?? []}
            selectTextStates={selectTextStates}
            setSelectTextStates={setSelectTextStates}
          />
          <BooleansInputs
            booleans={assistantChoosed.inputs.booleans ?? []}
            conditionalInputs={assistantChoosed.inputs.conditional_inputs}
            booleanStates={booleanStates}
            setBooleanStates={setBooleanStates}
            selectTextStates={selectTextStates}
          />
        </div>
      )}
      {assistantChoosed && (
        <div className={styles.buttons_wrapper}>
          <QuivrButton
            iconName="chevronLeft"
            label="Back"
            color="primary"
            onClick={() => handleBack()}
          />
          <QuivrButton
            iconName="chevronRight"
            label="EXECUTE"
            color="primary"
            important={true}
            onClick={handleSubmit}
            isLoading={loading}
            disabled={!isFormValid}
          />
        </div>
      )}
    </div>
  );
};

export default AssistantTab;
