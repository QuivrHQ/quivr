"use client";

import {
  Popover,
  PopoverTrigger,
  PopoverContent,
} from "@/ui/primitives/popover";
import { useContext } from "react";
import { AppContext } from "./providers";
import { Check, Menu as MenuIcon } from "lucide-react";

export default function Menu() {
  const { font: currentFont, setFont } = useContext(AppContext);

  return (
    <Popover>
      <PopoverTrigger className="absolute bottom-5 right-5 z-10 flex h-8 w-8 items-center justify-center rounded-lg transition-colors duration-200 hover:bg-stone-100 active:bg-stone-200 sm:bottom-auto sm:top-5">
        <MenuIcon className="text-stone-600" width={16} />
      </PopoverTrigger>
      <PopoverContent className="w-52" align="end">
        <div className="grid p-2">
          <div className="p-2">
            <p className="text-sm font-medium text-stone-500">Font Style</p>
          </div>
          {["Sans Serif", "Serif"].map((font) => (
            <button
              key={font}
              className="flex items-center justify-between rounded px-2 py-1 text-sm text-stone-600 hover:bg-stone-100"
              onClick={() => {
                setFont(font);
              }}
            >
              <div className="flex items-center space-x-2">
                <div className="rounded-sm border border-stone-200 p-1">Aa</div>
                <span>{font}</span>
              </div>
              {currentFont === font && <Check className="h-4 w-4" />}
            </button>
          ))}
        </div>
      </PopoverContent>
    </Popover>
  );
}
