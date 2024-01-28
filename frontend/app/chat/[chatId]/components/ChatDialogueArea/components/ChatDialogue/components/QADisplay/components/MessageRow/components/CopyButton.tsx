import Icon from "@/lib/components/ui/Icon/Icon";

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
    <Icon
      name={isCopied ? "checkCircle" : "copy"}
      color={isCopied ? "primary" : "black"}
      size="normal"
      handleHover={true}
    />
  </button>
);
