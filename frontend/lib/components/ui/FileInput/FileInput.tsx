import { useRef, useState } from "react";
import { Accept, useDropzone } from "react-dropzone";

import styles from "./FileInput.module.scss";

import { Icon } from "../Icon/Icon";

interface FileInputProps {
  label: string;
  onFileChange: (file: File) => void;
  acceptedFileTypes?: string[];
}

export const FileInput = (props: FileInputProps): JSX.Element => {
  const [currentFile, setCurrentFile] = useState<File | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (file: File) => {
    const fileExtension = file.name.split(".").pop();
    if (props.acceptedFileTypes?.includes(fileExtension || "")) {
      props.onFileChange(file);
      setCurrentFile(file);
      setErrorMessage("");
    } else {
      setErrorMessage("Wrong extension");
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      handleFileChange(file);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const mimeTypes: { [key: string]: string } = {
    pdf: "application/pdf",
    doc: "application/msword",
    docx: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    xls: "application/vnd.ms-excel",
    xlsx: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    csv: "text/csv",
    txt: "text/plain",
    jpg: "image/jpeg",
    jpeg: "image/jpeg",
    png: "image/png",
  };

  const accept: Accept | undefined = props.acceptedFileTypes?.reduce(
    (acc, type) => {
      const mimeType = mimeTypes[type];
      if (mimeType) {
        acc[mimeType] = [];
      }

      return acc;
    },
    {} as Accept
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles) => {
      const file = acceptedFiles[0];
      if (file) {
        handleFileChange(file);
      }
    },
    accept,
  });

  return (
    <div
      {...getRootProps()}
      className={`${styles.file_input_wrapper} ${
        isDragActive ? styles.drag_active : ""
      }`}
    >
      <div className={styles.header_wrapper} onClick={handleClick}>
        <div className={styles.box_content}>
          <Icon name="upload" size="big" color="black" />
          <div className={styles.input}>
            <div className={styles.clickable}>
              <span>Choose file</span>
            </div>
            <span>or drag it here</span>
          </div>
          {currentFile && (
            <span className={styles.filename}>{currentFile.name}</span>
          )}
        </div>
      </div>
      <input
        {...getInputProps()}
        ref={fileInputRef}
        type="file"
        className={styles.file_input}
        onChange={handleInputChange}
        style={{ display: "none" }}
      />
      {errorMessage !== "" && (
        <span className={styles.error_message}>{errorMessage}</span>
      )}
    </div>
  );
};
