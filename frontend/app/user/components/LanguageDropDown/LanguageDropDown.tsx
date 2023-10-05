import { FaLanguage } from "react-icons/fa";
import { MdCheck } from "react-icons/md";

import Popover from "@/lib/components/ui/Popover";

import { useLanguageHook } from "./hooks/useLanguageHook";

export const LanguageDropDown = (): JSX.Element => {
  const { allLanguages, currentLanguage, change } = useLanguageHook();

  return (
    <>
      {/* Add the brain icon and dropdown */}
      <div className="focus:outline-none text-3xl">
        <Popover
          Trigger={
            <button
              type="button"
              className="flex items-center focus:outline-none"
            >
              <FaLanguage className="w-6 h-6" />
            </button>
          }
          CloseTrigger={false}
        >
          <div>
            <div className="overflow-auto scrollbar flex flex-col h-48 mt-5">
              {Object.keys(allLanguages).map((lang) => {
                return (
                  <div key={lang} className="relative flex group items-center">
                    <button
                      type="button"
                      className={`flex flex-1 items-center gap-2 w-full text-left px-4 py-2 text-sm leading-5 text-gray-900 dark:text-gray-300 group-hover:bg-gray-100 dark:group-hover:bg-gray-700 group-focus:bg-gray-100 dark:group-focus:bg-gray-700 group-focus:outline-none transition-colors`}
                      onClick={() => {
                        change(lang);
                      }}
                    >
                      <span>
                        <MdCheck
                          style={{
                            opacity: currentLanguage === lang ? 1 : 0,
                          }}
                          className="text-xl transition-opacity"
                          width={32}
                          height={32}
                        />
                      </span>
                      <span className="flex-1">{allLanguages[lang].label}</span>
                    </button>
                  </div>
                );
              })}
            </div>
          </div>
        </Popover>
      </div>
    </>
  );
};
