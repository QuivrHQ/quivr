import { UUID } from "crypto";
import { useState } from "react";

import styles from "./SingleSelector.module.scss";

import { Icon } from "../Icon/Icon";
import { TextInput } from "../TextInput/TextInput";

export type SelectOptionProps<T> = {
  label: string;
  value: T;
};

type SelectProps<T> = {
  options: SelectOptionProps<T>[];
  onChange: (option: T) => void;
  selectedOption: SelectOptionProps<T> | undefined;
  placeholder: string;
};

export const SingleSelector = <T extends string | number | UUID>({
  onChange,
  options,
  selectedOption,
  placeholder,
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
      <div
        className={`${styles.first_line_wrapper} ${
          !folded ? styles.unfolded : ""
        }`}
      >
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
            `}
          >
            {selectedOption?.label ?? placeholder}
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
              className={styles.option}
              key={option.value.toString()}
              onClick={() => handleOptionClick(option)}
            >
              <div className={styles.icon}>
                <Icon name="brain" size="normal" color="black" />
              </div>
              <span className={styles.brain_name}>{option.label}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
