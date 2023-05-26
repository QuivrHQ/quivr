import { motion } from "framer-motion";
import { Dispatch, SetStateAction } from "react";
import { MdClose } from "react-icons/md";

export const FileComponent = ({
  file,
  setFiles,
}: {
  file: File;
  setFiles: Dispatch<SetStateAction<File[]>>;
}) => {
  return (
    <motion.div
      initial={{ x: "-10%", opacity: 0 }}
      animate={{ x: "0%", opacity: 1 }}
      exit={{ x: "10%", opacity: 0 }}
      className="flex flex-row gap-1 py-2 dark:bg-black border-b border-black/10 dark:border-white/25 leading-none px-6"
    >
      <div className="flex flex-1">
        <div className="flex flex flex-col">
          <span className="overflow-ellipsis overflow-hidden whitespace-nowrap">
            {file.name}
          </span>
          <span className="text-xs opacity-50 overflow-hidden text-ellipsis">
            {(file.size / 1000).toFixed(3)} kb
          </span>
        </div>
      </div>
      <div className="flex w-5">
        <button
          role="remove file"
          className="text-xl text-red-500 text-ellipsis"
          onClick={() =>
            setFiles((files) =>
              files.filter((f) => f.name !== file.name || f.size !== file.size)
            )
          }
        >
          <MdClose />
        </button>
      </div>
    </motion.div>
  );
};
