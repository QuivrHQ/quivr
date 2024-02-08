import { UUID } from "crypto";
import { useState } from "react";

import styles from "./SingleSelector.module.scss";

import Icon from "../Icon/Icon";
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
  const [folded, setFolded] = useState<boolean>(true);

  const filteredOptions = options.filter((option) =>
    option.label.toLowerCase().includes(search.toLowerCase())
  );

  const handleOptionClick = (option: SelectOptionProps<T>) => {
    onChange(option.value);
    setFolded(true);
  };

  return (
    <div className={styles.single_selector_wrapper}>
      <div className={styles.first_line_wrapper}>
        <div className={styles.left} onClick={() => setFolded(!folded)}>
          <div className={styles.icon}>
            <Icon
              name={folded ? "chevronDown" : "chevronRight"}
              size="normal"
              color="black"
            />
          </div>
          <div
            className={`
            ${styles.label} 
            ${!selectedOption ? styles.not_set : ""}
            ${!selectedOption && !folded ? styles.unfolded_not_set : ""}
            `}
          >
            {selectedOption?.label ?? "Choose a brain"}
          </div>
        </div>
        {!folded && (
          <div className={styles.right}>
            <TextInput
              label="Search..."
              inputValue={search}
              setInputValue={setSearch}
              simple={true}
            />
          </div>
        )}
      </div>
      {!folded && (
        <div className={styles.options}>
          {filteredOptions.map((option) => (
            <div
              key={option.value.toString()}
              onClick={() => handleOptionClick(option)}
            >
              {option.label}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
