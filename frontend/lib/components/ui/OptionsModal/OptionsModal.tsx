import { useEffect, useRef, useState } from "react";

import { Option } from "@/lib/types/Options";

import styles from "./OptionsModal.module.scss";

import { Icon } from "../Icon/Icon";

type OptionsModalProps = {
  options: Option[];
};

export const OptionsModal = ({ options }: OptionsModalProps): JSX.Element => {
  const [hovered, setHovered] = useState<boolean[]>(
    new Array(options.length).fill(false)
  );

  const handleMouseEnter = (index: number) => {
    setHovered((prevHovered) =>
      prevHovered.map((h, i) => (i === index ? true : h))
    );
  };

  const handleMouseLeave = (index: number) => {
    setHovered((prevHovered) =>
      prevHovered.map((h, i) => (i === index ? false : h))
    );
  };

  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    modalRef.current?.focus();
  }, []);

  return (
    <div className={styles.options_modal_wrapper} ref={modalRef} tabIndex={-1}>
      {options.map((option, index) => (
        <div
          className={`${styles.option} ${
            option.disabled ? styles.disabled : ""
          }`}
          key={index}
          onClick={option.onClick}
          onMouseEnter={() => handleMouseEnter(index)}
          onMouseLeave={() => handleMouseLeave(index)}
        >
          <span>{option.label}</span>
          <Icon
            name={option.iconName}
            color={hovered[index] ? option.iconColor : "black"}
            size="normal"
          />
        </div>
      ))}
    </div>
  );
};
