import { UUID } from "crypto";
import { useState } from "react";

import styles from "./SingleSelector.module.scss";

import { TextInput } from "../TextInput/TextInput";

export type SelectOptionProps<T> = {
  label: string;
  value: T;
};

type SelectProps<T> = {
  options: SelectOptionProps<T>[];
  onChange: (option: T) => void;
  selectedOption: SelectOptionProps<T> | undefined;
};

export const SingleSelector = <T extends string | number | UUID>({
  onChange,
  options,
  selectedOption,
}: SelectProps<T>): JSX.Element => {
  const [search, setSearch] = useState<string>("");

  const filteredOptions = options.filter((option) =>
    option.label.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className={styles.single_selector_wrapper}>
      <div className={styles.first_line_wrapper}>
        <div>{selectedOption?.label}</div>
        <TextInput
          iconName="search"
          label="Search"
          inputValue={search}
          setInputValue={setSearch}
        />
      </div>
      <div>
        {filteredOptions.map((option) => (
          <div
            key={option.value.toString()}
            onClick={() => onChange(option.value)}
          >
            {option.label}
          </div>
        ))}
      </div>
    </div>
  );
};
