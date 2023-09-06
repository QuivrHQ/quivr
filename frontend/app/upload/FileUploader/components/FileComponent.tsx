/* eslint-disable */
import { motion } from "framer-motion";
import { Dispatch, forwardRef, RefObject, SetStateAction } from "react";
import { MdClose } from "react-icons/md";

interface FileComponentProps {
  file: File;
  setFiles: Dispatch<SetStateAction<File[]>>;
}

const FileComponent = forwardRef(
  ({ file, setFiles }: FileComponentProps, forwardedRef) => {
    return (
      <motion.div
        initial={{ x: "-10%", opacity: 0 }}
        animate={{ x: "0%", opacity: 1 }}
        exit={{ x: "10%", opacity: 0 }}
        layout
        ref={forwardedRef as RefObject<HTMLDivElement>}
        className="relative flex flex-row gap-1 py-2 dark:bg-black border-b last:border-none border-black/10 dark:border-white/25 leading-none px-6 overflow-hidden"
      >
        <div className="flex flex-1">
          <div className="flex flex-col">
            <span className="overflow-ellipsis overflow-hidden whitespace-nowrap">
              {file.name}
            </span>
            <span className="text-xs opacity-50 overflow-hidden text-ellipsis">
              {(file.size / 1000).toFixed(3)} kb
            </span>
          </div>
        </div>
        <button
          role="remove file"
          className="text-xl text-red-500 text-ellipsis absolute top-0 h-full right-0 flex items-center justify-center bg-white dark:bg-black p-3 shadow-md aspect-square"
          onClick={() =>
            setFiles((files) => files.filter((f) => f.name !== file.name))
          }
        >
          <MdClose />
        </button>
      </motion.div>
    );
  }
);

FileComponent.displayName = "FileComponent";

export default FileComponent;
