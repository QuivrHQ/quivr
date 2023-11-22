"use client";

// eslint-disable-next-line import/no-extraneous-dependencies
import { Listbox, Transition } from "@headlessui/react";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/react/20/solid";
import { Fragment } from "react";
import { IoLanguage } from "react-icons/io5";

import {
  languages,
  useLanguageHook,
} from "@/app/user/components/LanguageDropDown/hooks/useLanguageHook";
import { cn } from "@/lib/utils";

export const LanguageSelect = ({
  isSelect,
}: {
  isSelect?: boolean;
}): JSX.Element => {
  const { allLanguages, currentLanguage, change, handleToggleLanguage } =
    useLanguageHook();

  return (
    <div className={`${!isSelect ? "mr-4 ml-2" : "py-2 mx-4"}`}>
      {isSelect && (
        <Listbox
          value={currentLanguage}
          onChange={(e) => {
            change(e);
          }}
        >
          {({ open }) => (
            <>
              <div className="relative">
                <Listbox.Button className="text-xs relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-8 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                  <span className="block truncate">
                    {Object.keys(allLanguages).length > 0 &&
                    currentLanguage !== undefined
                      ? allLanguages[currentLanguage].label
                      : languages["en"].label}
                  </span>
                  <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon
                      className="h-5 w-5 text-gray-400"
                      aria-hidden="true"
                    />
                  </span>
                </Listbox.Button>

                <Transition
                  show={open}
                  as={Fragment}
                  leave="transition ease-in duration-100"
                  leaveFrom="opacity-100"
                  leaveTo="opacity-0"
                >
                  <Listbox.Options className="absolute z-10 mt-1 max-h-60 w-36 overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    {Object.keys(allLanguages).map((lang) => (
                      <Listbox.Option
                        key={lang}
                        className={({ active }) =>
                          cn(
                            active
                              ? "bg-indigo-600 text-white"
                              : "text-gray-900",
                            "relative cursor-default select-none py-2 pl-3 pr-9 text-xs sm:text-sm"
                          )
                        }
                        value={lang}
                      >
                        {({ selected, active }) => (
                          <>
                            <span
                              className={cn(
                                selected ? "font-semibold" : "font-normal",
                                "block truncate"
                              )}
                            >
                              {allLanguages[lang].label}
                            </span>

                            {selected ? (
                              <span
                                className={cn(
                                  active ? "text-white" : "text-indigo-600",
                                  "absolute inset-y-0 right-0 flex items-center pr-2"
                                )}
                              >
                                <CheckIcon
                                  className="h-5 w-5"
                                  aria-hidden="true"
                                />
                              </span>
                            ) : null}
                          </>
                        )}
                      </Listbox.Option>
                    ))}
                  </Listbox.Options>
                </Transition>
              </div>
            </>
          )}
        </Listbox>
      )}
      {!isSelect && (
        <div>
          <button
            onClick={() => handleToggleLanguage()}
            className="text-white hover:text-slate-200 cursor-pointer  text-xs  bg-transparent py-1.5 px-3 text-left   sm:text-sm sm:leading-6"
          >
            <IoLanguage className="" />
          </button>
        </div>
      )}
    </div>
  );
};
