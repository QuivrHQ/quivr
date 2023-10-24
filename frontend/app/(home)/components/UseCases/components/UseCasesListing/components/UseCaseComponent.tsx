import { Fragment } from "react";
import { PiPaperclipFill } from "react-icons/pi";

import { UseCase } from "@/lib/types/UseCase";

type UseCaseComponentProps = {
  discussions: UseCase["discussions"];
};

export const UseCaseComponent = ({
  discussions,
}: UseCaseComponentProps): JSX.Element => {
  return (
    <div className="flex flex-col gap-2 text-black">
      {discussions.map((d) => (
        <Fragment key={d.question}>
          <div className="flex justify-end">
            <div className="bg-[#9B9B9B] max-w-[75%] bg-opacity-10 p-4 rounded-xl">
              <p>{d.question}</p>
            </div>
          </div>
          <div className="flex">
            <div className="bg-[#E0DDFC] max-w-[75%] rounded-xl p-4">
              <span className="text-[#8F8F8F] text-xs">@Quivr</span>
              <p>{d.answer}</p>
            </div>
          </div>
        </Fragment>
      ))}
      <div className="flex flex-col w-full shadow-md dark:shadow-primary/25 hover:shadow-xl transition-shadow rounded-xl bg-white dark:bg-black border border-black/10 dark:border-white/25 p-4 mt-10">
        <div className="flex items-center">
          <PiPaperclipFill className="text-3xl" />
          <span className="text-[#BFBFBF]">@Einstein</span>
        </div>
      </div>
    </div>
  );
};
