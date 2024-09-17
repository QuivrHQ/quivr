import { useRef, useState } from "react";

import styles from "./FileInput.module.scss";

import { Icon } from "../Icon/Icon";

interface FileInputProps {
  label: string;
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
    <div className={styles.file_input_wrapper} onClick={handleClick}>
      <div className={styles.header_wrapper}>
        <div className={styles.box_content}>
          <Icon name="upload" size="big" color="black" />
          <div className={styles.input}>
            <div className={styles.clickable}>
              <span>Choose files</span>
            </div>
            <span>or drag it here</span>
          </div>
        </div>
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
      {currentFile && (
        <span className={styles.filename}>{currentFile.name}</span>
      )}
      {errorMessage !== "" && (
        <span className={styles.error_message}>{errorMessage}</span>
      )}
    </div>
  );
};
