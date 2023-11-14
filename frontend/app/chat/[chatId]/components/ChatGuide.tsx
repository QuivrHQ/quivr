"use client";
import Image from "next/image";

import { Disclaimer } from "@/lib/components/Disclaimer";
export const ChatGuide = (): JSX.Element => {
  return (
    <div className="flex flex-col justify-center items-center h-full">
      <Disclaimer />
      <div className="flex-1 flex flex-col justify-center items-center">
        <Image
          className="rounded-full w-16 h-16 mb-4"
          src={"/vt-logo.png"}
          alt="vaccinetruth.ai logo"
          height={100}
          width={100}
        ></Image>

        <div className="font-bold mb-2">Vaccine Truth AI ChatBot</div>
        <div className="text-xs text-slate-500">I am a chat bot</div>
      </div>
    </div>
  );
};
