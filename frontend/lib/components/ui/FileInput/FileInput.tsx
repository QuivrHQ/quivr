import { useRef, useState } from "react";

import { iconList } from "@/lib/helpers/iconList";

import styles from "./FileInput.module.scss";

import { FieldHeader } from "../FieldHeader/FieldHeader";
import { Icon } from "../Icon/Icon";

interface FileInputProps {
  label: string;
  icon: keyof typeof iconList;
  onFileChange: (file: File) => void;
  acceptedFileTypes?: string[];
}

export const FileInput = (props: FileInputProps): JSX.Element => {
  const [currentFile, setcurrentFile] = useState<File | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const fileExtension = file.name.split(".").pop();
      if (props.acceptedFileTypes?.includes(fileExtension || "")) {
        props.onFileChange(file);
        setcurrentFile(file);
        setErrorMessage("");
      } else {
        setErrorMessage("Wrong extension");
      }
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
            Click here to {currentFile ? "change your" : "upload a"} file
          </span>
          <Icon name="upload" size="normal" color="black" />
        </div>
        <input
          ref={fileInputRef}
          type="file"
          className={styles.file_input}
          onChange={handleFileChange}
          accept={props.acceptedFileTypes
            ?.map((type) => `application/${type}`)
            .join(",")}
          style={{ display: "none" }}
        />
      </div>
      {currentFile && (
        <span className={styles.filename}>{currentFile.name}</span>
      )}
      {errorMessage !== "" && (
        <span className={styles.error_message}>{errorMessage}</span>
      )}
    </div>
  );
};
