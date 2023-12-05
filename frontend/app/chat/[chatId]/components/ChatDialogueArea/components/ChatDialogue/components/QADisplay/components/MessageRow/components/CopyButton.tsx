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
    className="text-white hover:text-sky-600 transition"
    onClick={handleCopy}
    title={isCopied ? "Copied!" : "Copy to clipboard"}
  >
    {isCopied ? <FaCheckCircle /> : <FaCopy />}
  </button>
);
