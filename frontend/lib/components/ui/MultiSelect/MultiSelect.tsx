import { UUID } from "crypto";
import { useState } from "react";

import { iconList } from "@/lib/helpers/iconList";

import styles from "./MultiSelect.module.scss";

import { Icon } from "../Icon/Icon";
import { TextInput } from "../TextInput/TextInput";

export type SelectOptionProps<T> = {
  label: string;
  value: T;
};

type MultiSelectProps<T> = {
  options: SelectOptionProps<T>[];
  onChange: (selectedOptions: T[]) => void | Promise<void>;
  selectedOptions: SelectOptionProps<T>[];
  placeholder: string;
  iconName: keyof typeof iconList;
  onBackClick?: () => void;
};

export const MultiSelect = <T extends string | number | UUID>({
  onChange,
  options,
  selectedOptions,
  placeholder,
  iconName,
  onBackClick,
}: MultiSelectProps<T>): JSX.Element => {
  const [search, setSearch] = useState<string>("");
  const [folded, setFolded] = useState<boolean>(true);
  const [updating, setUpdating] = useState<boolean>(false);

  const filteredOptions = options.filter((option) =>
    option.label.toLowerCase().includes(search.toLowerCase())
  );

  const handleOptionClick = async (option: SelectOptionProps<T>) => {
    try {
      if (!updating) {
        setUpdating(true);
        const isSelected = selectedOptions.some(
          (selected) => selected.value === option.value
        );
        
        let newSelectedOptions: T[];
        
        if (isSelected) {
          // Remove option if already selected
          newSelectedOptions = selectedOptions
            .filter((selected) => selected.value !== option.value)
            .map((selected) => selected.value);
        } else {
          // Add option if not already selected
          newSelectedOptions = [
            ...selectedOptions.map((selected) => selected.value),
            option.value,
          ];
        }
        
        await onChange(newSelectedOptions);
        setUpdating(false);
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className={styles.multi_selector_wrapper}>
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
          {folded && (
            <div
              className={`
                ${styles.label} 
                ${selectedOptions.length === 0 ? styles.not_set : ""}
              `}
            >
              <span className={styles.label_text}>
                {selectedOptions.length > 0
                  ? `${selectedOptions.length} selected`
                  : placeholder}
              </span>
            </div>
          )}
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
          {filteredOptions.map((option) => {
            const isSelected = selectedOptions.some(
              (selected) => selected.value === option.value
            );
            
            return (
              <div
                className={`${styles.option} ${isSelected ? styles.selected : ""}`}
                key={option.value.toString()}
                onClick={() => {
                  handleOptionClick(option).catch(console.error);
                }}
              >
                <div className={styles.icon}>
                  <Icon name={iconName} size="small" color="black" />
                </div>
                <span className={styles.option_name}>{option.label}</span>
                {isSelected && (
                  <div className={styles.check_icon}>
                    <Icon name="check" size="small" color="black" />
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
