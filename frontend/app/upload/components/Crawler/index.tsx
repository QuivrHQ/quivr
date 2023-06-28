"use client";
import Button from "@/lib/components/ui/Button";
import Card from "@/lib/components/ui/Card";
import Field from "@/lib/components/ui/Field";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { useCrawler } from "./hooks/useCrawler";

export const Crawler = (): JSX.Element => {
  const { urlInputRef, isCrawling, crawlWebsite } = useCrawler();
  const { currentBrain } = useBrainContext();

  return (
    <div className="w-full">
      <div className="flex justify-center gap-5 px-6">
        <div className="max-w-xl w-full">
          <div className="flex-col justify-center gap-5">
            <Card className="h-32 flex gap-5 justify-center items-center px-5">
              <div className="text-center max-w-sm w-full flex flex-col gap-5 items-center">
                <Field
                  name="crawlurl"
                  ref={urlInputRef}
                  type="text"
                  placeholder="Enter a website URL"
                  className="w-full"
                />
              </div>
              <div className="flex flex-col items-center justify-center gap-5">
                <Button
                  isLoading={isCrawling}
                  onClick={() => void crawlWebsite(currentBrain?.id)}
                >
                  Crawl
                </Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};
