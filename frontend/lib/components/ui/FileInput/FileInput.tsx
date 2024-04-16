import { useRef, useState } from "react";

import { iconList } from "@/lib/helpers/iconList";

import styles from "./FileInput.module.scss";

import { FieldHeader } from "../FieldHeader/FieldHeader";
import { Icon } from "../Icon/Icon";

interface FileInputProps {
  label: string;
  icon: keyof typeof iconList;
  onFileChange: (file: File) => void;
}

export const FileInput = (props: FileInputProps): JSX.Element => {
  const [currentFile, setCurrentFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      props.onFileChange(file);
      setCurrentFile(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div>
      <FieldHeader label={props.label} iconName={props.icon.toString()} />
      <div className={styles.file_input_wrapper} onClick={handleClick}>
        <div className={styles.header_wrapper}>
          <span className={styles.placeholder}>
            Click here to upload a file
          </span>
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
      {currentFile && (
        <span className={styles.filename}>{currentFile.name}</span>
      )}
    </div>
  );
};
