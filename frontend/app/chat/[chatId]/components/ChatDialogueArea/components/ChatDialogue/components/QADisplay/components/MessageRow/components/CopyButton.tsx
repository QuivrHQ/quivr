import { FaCheckCircle, FaCopy } from "react-icons/fa";

type CopyButtonProps = {
  handleCopy: () => void;
  isCopied: boolean;
};

export const CopyButton = ({
  handleCopy,
  isCopied,
}: CopyButtonProps): JSX.Element => (
  <button
    className="text-gray-500 hover:text-gray-700 transition"
    onClick={handleCopy}
    title={isCopied ? "Copied!" : "Copy to clipboard"}
  >
    {isCopied ? <FaCheckCircle /> : <FaCopy />}
  </button>
);
