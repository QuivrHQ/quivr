import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useTranslation } from "react-i18next";
import { LuChevronRight } from "react-icons/lu";

import { useHomepageTracking } from "@/app/(home)/hooks/useHomepageTracking";
import { DEMO_VIDEO_DATA_KEY } from "@/lib/api/cms/config";
import { useCmsApi } from "@/lib/api/cms/useCmsApi";
import Button from "@/lib/components/ui/Button";
import Spinner from "@/lib/components/ui/Spinner";

import { VideoPlayer } from "./components/VideoPlayer";

export const DemoSection = (): JSX.Element => {
  const { t } = useTranslation("home", { keyPrefix: "demo" });
  const { getDemoVideoUrl } = useCmsApi();
  const { onLinkClick } = useHomepageTracking();
  const { data: demoVideoUrl } = useQuery({
    queryKey: [DEMO_VIDEO_DATA_KEY],
    queryFn: getDemoVideoUrl,
  });

  return (
    <div className="sm:min-h-[calc(100vh-250px)] flex flex-col items-center justify-center gap-10">
      <h2 className="text-center text-3xl font-semibold mb-5">{t("title")}</h2>
      <div className="max-w-4xl">
        {demoVideoUrl !== undefined ? (
          <VideoPlayer videoSrc={demoVideoUrl} />
        ) : (
          <Spinner />
        )}
      </div>
      <Link
        href="/signup"
        onClick={(event) => {
          onLinkClick({
            href: "/signup",
            label: "SIGN_UP",
            event,
          });
        }}
      >
        <Button className="mt-2 rounded-full">
          {t("start_now")} <LuChevronRight size={24} />
        </Button>
      </Link>
    </div>
  );
};
