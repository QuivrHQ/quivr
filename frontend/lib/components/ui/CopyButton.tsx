import { useEffect, useState } from "react";

import Icon from "@/lib/components/ui/Icon/Icon";

type CopyButtonProps = {
  handleCopy: () => void;
};

export const CopyButton = ({ handleCopy }: CopyButtonProps): JSX.Element => {
  const [isCopied, setIsCopied] = useState(false);

  const handleClick = () => {
    handleCopy();
    setIsCopied(true);
  };

  useEffect(() => {
    if (isCopied) {
      const timer = setTimeout(() => {
        setIsCopied(false);
      }, 2000);

      return () => {
        clearTimeout(timer);
      };
    }
  }, [isCopied]);

  return (
    <button
      className="text-gray-500 hover:text-gray-700 transition"
      onClick={handleClick}
      title={isCopied ? "Copied!" : "Copy to clipboard"}
    >
      <Icon
        name={isCopied ? "checkCircle" : "copy"}
        color={isCopied ? "primary" : "black"}
        size="small"
        handleHover={true}
      />
    </button>
  );
};
