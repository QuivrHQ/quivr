import { useTranslation } from "react-i18next";
import { MdClose } from "react-icons/md";

import Button from "@/lib/components/ui/Button";
import { Divider } from "@/lib/components/ui/Divider";

import { Crawler } from "./components/Crawler";
import { FileUploader } from "./components/FileUploader";

type FeedProps = {
  onClose: () => void;
};
export const Feed = ({ onClose }: FeedProps): JSX.Element => {
  const { t } = useTranslation(["translation"]);

  return (
    <div className="flex flex-col w-full relative">
      <div className="absolute right-2 top-1">
        <Button variant={"tertiary"} onClick={onClose}>
          <span>
            <MdClose className="text-3xl" />
          </span>
        </Button>
      </div>
      <FileUploader />
      <Divider text={t("or")} className="m-5" />
      <Crawler />
    </div>
  );
};
