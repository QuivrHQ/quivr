import { UUID } from "crypto";
import { useState } from "react";

import { iconList } from "@/lib/helpers/iconList";

import styles from "./SingleSelector.module.scss";

import { Icon } from "../Icon/Icon";
import { TextInput } from "../TextInput/TextInput";

export type SelectOptionProps<T> = {
  label: string;
  value: T;
};

type SelectProps<T> = {
  options: SelectOptionProps<T>[];
  onChange: (option: T) => void | Promise<void>;
  selectedOption: SelectOptionProps<T> | undefined;
  placeholder: string;
  iconName: keyof typeof iconList;
  onBackClick?: () => void;
};

export const SingleSelector = <T extends string | number | UUID>({
  onChange,
  options,
  selectedOption,
  placeholder,
  iconName,
  onBackClick,
}: SelectProps<T>): JSX.Element => {
  const [search, setSearch] = useState<string>("");
  const [folded, setFolded] = useState<boolean>(true);
  const [updating, setUpdating] = useState<boolean>(false);

  const filteredOptions = options.filter((option) =>
    option.label.toLowerCase().includes(search.toLowerCase())
  );

  const handleOptionClick = async (option: SelectOptionProps<T>) => {
    try {
      if (option !== selectedOption && !updating) {
        setUpdating(true);
        await onChange(option.value);
        setUpdating(false);
      }
      setFolded(true);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className={styles.single_selector_wrapper}>
      <div
        className={`${styles.first_line_wrapper} ${
          !folded ? styles.unfolded : ""
        }`}
      >
        <div
          className={styles.left}
          onClick={() => {
            setFolded(!folded);
            if (!folded) {
              onBackClick?.();
            }
          }}
        >
          <div className={styles.icon}>
            <Icon
              name={
                folded ? "chevronDown" : onBackClick ? "back" : "chevronRight"
              }
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
              onClick={() => {
                handleOptionClick(option).catch(console.error);
              }}
            >
              <div className={styles.icon}>
                <Icon name={iconName} size="normal" color="black" />
              </div>
              <span className={styles.option_name}>{option.label}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
