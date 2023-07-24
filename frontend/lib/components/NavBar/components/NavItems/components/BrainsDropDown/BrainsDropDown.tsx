import { useState } from "react";
import { FaBrain } from "react-icons/fa";
import { MdCheck } from "react-icons/md";

import Field from "@/lib/components/ui/Field";
import Popover from "@/lib/components/ui/Popover";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

import { BrainActions } from "./components/BrainActions/BrainActions";
import { AddBrainModal } from "../../../../../AddBrainModal/AddBrainModal";

export const BrainsDropDown = (): JSX.Element => {
  const [searchQuery, setSearchQuery] = useState("");
  const { allBrains, isFetchingBrains, setActiveBrain, currentBrain } =
    useBrainContext();

  return (
    <>
      {/* Add the brain icon and dropdown */}
      <div className="relative ml-auto px-4 py-2">
        <Popover
          Trigger={
            <button
              type="button"
              className="flex items-center focus:outline-none"
            >
              <FaBrain className="w-6 h-6" />
            </button>
          }
          ActionTrigger={<AddBrainModal />}
          CloseTrigger={false}
        >
          <div>
            <Field
              name="brainsearch"
              placeholder="Search for a brain"
              autoFocus
              autoComplete="off"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <div className="overflow-auto scrollbar flex flex-col h-48 mt-5">
              {/* List of brains */}
              {isFetchingBrains && (
                <div className="flex items-center justify-center h-full">
                  <p className="text-gray-500">Loading...</p>
                </div>
              )}
              {allBrains.map((brain) => {
                if (brain.name.includes(searchQuery)) {
                  return (
                    <div
                      key={brain.id}
                      className="relative flex group items-center"
                    >
                      <button
                        type="button"
                        className={`flex flex-1 items-center gap-2 w-full text-left px-4 py-2 text-sm leading-5 text-gray-900 dark:text-gray-300 group-hover:bg-gray-100 dark:group-hover:bg-gray-700 group-focus:bg-gray-100 dark:group-focus:bg-gray-700 group-focus:outline-none transition-colors`}
                        onClick={() => {
                          setActiveBrain({ ...brain });
                          setSearchQuery("");
                        }}
                      >
                        <span>
                          <MdCheck
                            style={{
                              opacity: currentBrain?.id === brain.id ? 1 : 0,
                            }}
                            className="text-xl transition-opacity"
                            width={32}
                            height={32}
                          />
                        </span>
                        <span className="flex-1">{brain.name}</span>
                      </button>
                      <BrainActions brain={brain} />
                    </div>
                  );
                }
              })}
            </div>
          </div>
        </Popover>
      </div>
    </>
  );
};
