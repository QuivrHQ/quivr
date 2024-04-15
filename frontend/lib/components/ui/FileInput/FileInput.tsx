import { useRef } from "react";

import { iconList } from "@/lib/helpers/iconList";

import styles from "./FileInput.module.scss";

import { Icon } from "../Icon/Icon";

interface FileInputProps {
  label: string;
  icon: keyof typeof iconList;
  onFileChange: (file: File) => void;
}

export const FileInput = (props: FileInputProps): JSX.Element => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      props.onFileChange(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className={styles.file_input_wrapper}>
      <div className={styles.header_wrapper} onClick={handleClick}>
        <div className={styles.header_left}>
          <Icon name={props.icon} size="normal" color="primary" />
          <p className={styles.header_title}>{props.label}</p>
        </div>
        <Icon name="upload" size="normal" color="black" />
      </div>
      <input
        ref={fileInputRef}
        type="file"
        className={styles.file_input}
        onChange={handleFileChange}
        style={{ display: "none" }}
      />
    </div>
  );
};
