import React from "react";

import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";

import styles from "./SelectorsInputs.module.scss";

interface SelectorsInputsProps {
  selectTexts: { key: string; options: string[] }[];
  selectTextStates: { [key: string]: string | null };
  setSelectTextStates: React.Dispatch<
    React.SetStateAction<{ [key: string]: string | null }>
  >;
}

const SelectorsInputs = ({
  selectTexts,
  selectTextStates,
  setSelectTextStates,
}: SelectorsInputsProps): JSX.Element => {
  const handleSelectTextChange = (key: string, value: string) => {
    setSelectTextStates((prevState) => ({
      ...prevState,
      [key]: value,
    }));
  };

  return (
    <div className={styles.select_texts_wrapper}>
      {selectTexts.map((input, index) => (
        <div key={index} className={styles.select_text}>
          <SingleSelector
            iconName="brain"
            placeholder={input.key}
            options={input.options.map((option) => {
              return { label: option, value: option };
            })}
            onChange={(value) => handleSelectTextChange(input.key, value)}
            selectedOption={{
              label: selectTextStates[input.key] ?? input.options[0],
              value: selectTextStates[input.key] ?? input.options[0],
            }}
          />
        </div>
      ))}
    </div>
  );
};

export default SelectorsInputs;
