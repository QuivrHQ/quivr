/* eslint-disable */
import { useEffect, useRef, useState } from "react";
import { FaBrain } from "react-icons/fa";
import { IoMdAdd } from "react-icons/io";

import Button from "@/lib/components/ui/Button";
import Field from "@/lib/components/ui/Field";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useEventTracking } from "@/services/analytics/useEventTracking";
import { AnimatePresence, motion } from "framer-motion";
import { MdCheck } from "react-icons/md";

export const BrainsDropDown = (): JSX.Element => {
  const [showDropdown, setShowDropdown] = useState(false);
  const [newBrainName, setNewBrainName] = useState("");
  const { allBrains, createBrain, setActiveBrain, currentBrain } =
    useBrainContext();
  const dropdownRef = useRef<HTMLDivElement | null>(null);
  const { track } = useEventTracking();

  const toggleDropdown = () => {
    setShowDropdown((prevState) => !prevState);
    void track("SHOW_BRAINS_DROPDOWN");
  };

  const handleCreateBrain = () => {
    if (newBrainName.trim() === "") {
      return;
    }

    void createBrain(newBrainName);
    setNewBrainName(""); // Reset the new brain name input
    void track("BRAIN_CREATED");
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node | null)
    ) {
      setShowDropdown(false);
    }
  };

  const changeBrains = (value: string) => {
    void track("CHANGE_BRAIN");
    setNewBrainName(value);
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <>
      {/* Add the brain icon and dropdown */}
      <div className="relative ml-auto px-4 py-2" ref={dropdownRef}>
        <button
          type="button"
          className="flex items-center focus:outline-none"
          onClick={toggleDropdown}
        >
          <FaBrain className="w-6 h-6" />
        </button>
        <AnimatePresence>
          {showDropdown && (
            <motion.div
              initial={{ opacity: 0, y: -32, height: "0" }}
              animate={{
                opacity: 1,
                y: 0,
                height: "13rem",
              }}
              exit={{ opacity: 0, y: -32, height: "0" }}
              transition={{ duration: 0.2, ease: "easeInOut" }}
              className="absolute right-0 mt-2 w-96 flex flex-col bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg"
            >
              {/* Option to create a new brain */}
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleCreateBrain();
                }}
                className="flex items-center gap-2 p-2"
              >
                <Field
                  name="brainname"
                  placeholder="Add a new brain"
                  autoFocus
                  onChange={(e) => changeBrains(e.target.value)}
                />
                <Button type="submit" className="px-2 py-2">
                  <IoMdAdd className="w-5 h-5" />
                </Button>
              </form>
              <div className="overflow-auto scrollbar flex flex-col h-full">
                {/* List of brains */}
                {allBrains.map((brain) => (
                  <button
                    key={brain.id}
                    type="button"
                    className={`flex items-center gap-2 w-full text-left px-4 py-2 text-sm leading-5 text-gray-900 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:bg-gray-100 dark:focus:bg-gray-700 focus:outline-none`}
                    onClick={() => setActiveBrain({ ...brain })}
                  >
                    <span className="flex-1">{brain.name}</span>
                    <span>
                      {currentBrain?.id === brain.id && (
                        <MdCheck className="text-xl" width={32} height={32} />
                      )}
                    </span>
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </>
  );
};
