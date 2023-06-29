import { useEffect, useRef, useState } from "react";
import { FaBrain } from "react-icons/fa";
import { IoMdAdd } from "react-icons/io";

import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";

export const BrainsDropDown = (): JSX.Element => {
  const [showDropdown, setShowDropdown] = useState(false);
  const [newBrainName, setNewBrainName] = useState("");
  const { allBrains, createBrain, setActiveBrain, currentBrain } =
    useBrainContext();
  const dropdownRef = useRef<HTMLDivElement | null>(null);

  const toggleDropdown = () => {
    setShowDropdown((prevState) => !prevState);
  };

  const handleCreateBrain = () => {
    if (newBrainName.trim() === "") {
      return;
    }

    void createBrain(newBrainName);
    setNewBrainName(""); // Reset the new brain name input
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node | null)
    ) {
      setShowDropdown(false);
    }
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
        {showDropdown && (
          <div className="absolute overflow-scroll right-0 mt-2 w-96 h-52 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg">
            {/* Option to create a new brain */}
            <div className="px-4 py-2">
              <div className="flex items-center">
                <input
                  type="text"
                  placeholder="Add a new brain"
                  value={newBrainName}
                  onChange={(e) => setNewBrainName(e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none"
                />
                <button
                  type="button"
                  className="flex-shrink-0 ml-2 px-3 py-2 text-sm font-medium leading-5 text-white transition-colors duration-200 transform bg-blue-600 border border-transparent rounded-lg hover:bg-blue-500 focus:outline-none focus:bg-blue-500"
                  onClick={handleCreateBrain}
                >
                  <IoMdAdd className="w-5 h-5" />
                </button>
              </div>
            </div>
            {/* List of brains */}
            {allBrains.map((brain) => (
              <button
                key={brain.id}
                type="button"
                className={`block w-full text-left px-4 py-2 text-sm leading-5 ${
                  currentBrain?.id === brain.id ? "bg-blue-100" : ""
                } text-gray-900 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:bg-gray-100 dark:focus:bg-gray-700 focus:outline-none`}
                onClick={() => setActiveBrain({ ...brain })}
              >
                {brain.name}
              </button>
            ))}
          </div>
        )}
      </div>
    </>
  );
};
