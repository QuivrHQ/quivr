import { useRef, useState } from "react";
import { Accept, useDropzone } from "react-dropzone";

import styles from "./FileInput.module.scss";

import { Icon } from "../Icon/Icon";

interface FileInputProps {
  label: string;
  onFileChange: (files: File[]) => void;
  acceptedFileTypes?: string[];
  hideFileName?: boolean;
  handleMultipleFiles?: boolean;
}

export const FileInput = (props: FileInputProps): JSX.Element => {
  const [currentFiles, setCurrentFiles] = useState<File[]>([]);
  const [errorMessage, setErrorMessage] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (files: File[]) => {
    const validFiles = files.filter((file) => {
      const fileExtension = file.name.split(".").pop();

      return props.acceptedFileTypes?.includes(fileExtension ?? "");
    });

    if (validFiles.length > 0) {
      props.onFileChange(validFiles);
      setCurrentFiles(validFiles);
      setErrorMessage("");
    } else {
      setErrorMessage("Wrong extension");
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files ?? []);
    if (files.length > 0) {
      handleFileChange(files);
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
      handleFileChange(acceptedFiles);
    },
    accept,
    multiple: props.handleMultipleFiles,
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
          {currentFiles.length > 0 && !props.hideFileName && (
            <div className={styles.filename}>
              {currentFiles.map((file, index) => (
                <span key={index}>{file.name}</span>
              ))}
            </div>
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
        multiple={props.handleMultipleFiles}
      />
      {errorMessage !== "" && (
        <span className={styles.error_message}>{errorMessage}</span>
      )}
    </div>
  );
};
