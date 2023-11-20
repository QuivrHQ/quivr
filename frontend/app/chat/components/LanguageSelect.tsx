"use client";

// eslint-disable-next-line import/no-extraneous-dependencies
import { Listbox, Transition } from "@headlessui/react";
import { CheckIcon } from "@heroicons/react/20/solid";
import { Fragment } from "react";
import { IoLanguage } from "react-icons/io5";

import { useLanguageHook } from "@/app/user/components/LanguageDropDown/hooks/useLanguageHook";
import { cn } from "@/lib/utils";

export const LanguageSelect = (): JSX.Element => {
  const { allLanguages, currentLanguage, change } = useLanguageHook();

  return (
    <div className={`mr-4 ml-2`}>
      <Listbox
        value={currentLanguage}
        onChange={(e) => {
          change(e);
        }}
      >
        {({ open }) => (
          <>
            <div className="relative">
              <Listbox.Button className="hover:text-slate-400 cursor-pointer hover:bg-slate-50 text-xs relative cursor-default rounded-md bg-white py-1.5 px-3 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300  sm:text-sm sm:leading-6">
                <IoLanguage className="" />
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
                          active ? "bg-indigo-600 text-white" : "text-gray-900",
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
    </div>
  );
};
