import Link from "next/link";
import { useTranslation } from "react-i18next";
import { LuChevronRight } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";

import { VideoPlayer } from "./components/VideoPlayer";

export const DemoSection = (): JSX.Element => {
  const { t } = useTranslation("home", { keyPrefix: "demo" });

  return (
    <div className="sm:min-h-[calc(100vh-250px)] flex flex-col items-center justify-center gap-10">
      <h2 className="text-center text-3xl font-semibold mb-5">{t("title")}</h2>
      <div className="max-w-4xl">
        <VideoPlayer videoSrc="https://user-images.githubusercontent.com/19614572/239713902-a6463b73-76c7-4bc0-978d-70562dca71f5.mp4" />
      </div>
      <Link href="/signup">
        <Button className="mt-2 rounded-full">
          {t("start_now")} <LuChevronRight size={24} />
        </Button>
      </Link>
    </div>
  );
};
