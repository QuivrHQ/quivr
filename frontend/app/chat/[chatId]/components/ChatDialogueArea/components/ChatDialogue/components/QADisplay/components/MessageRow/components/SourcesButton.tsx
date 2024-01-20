import { useEffect, useRef, useState } from "react";
import ReactDOM from "react-dom";
import { FaQuestionCircle } from "react-icons/fa";

import { useEventTracking } from "@/services/analytics/june/useEventTracking";

type SourcesButtonProps = {
  sources: [string] | [];
};

export const SourcesButton = ({ sources }: SourcesButtonProps): JSX.Element => {
  const [showSources, setShowSources] = useState(false);
  const [popupPosition, setPopupPosition] = useState({ top: 0, left: 0 });
  const { track } = useEventTracking();
  // Specify the type of element the ref will be attached to
  const buttonRef = useRef<HTMLButtonElement>(null);

  const updatePopupPosition = () => {
    // Use the 'current' property of the ref with the correct type
    if (buttonRef.current) {
      const rect = buttonRef.current.getBoundingClientRect();
      setPopupPosition({
        top: rect.bottom + window.scrollY,
        left: rect.left + window.scrollX,
      });
    }
  };

  useEffect(() => {
    window.addEventListener("scroll", updatePopupPosition);

    // Remove the event listener when the component is unmounted
    return () => {
      window.removeEventListener("scroll", updatePopupPosition);
    };
  }, []);

  const sourcesList = (
    <ul className="list-disc list-inside">
      {sources.map((source, index) => (
        <li key={index} className="truncate">
          {source.trim()}
        </li>
      ))}
    </ul>
  );

  return (
    <div className="relative inline-block">
      <button
        ref={buttonRef} // Attach the ref to the button
        onMouseEnter={() => {
          setShowSources(true);
          updatePopupPosition();
          void track("SOURCE_CHECKED");
        }}
        onMouseLeave={() => setShowSources(false)}
        className="text-gray-500 hover:text-gray-700 transition p-1"
        title="View sources"
      >
        <FaQuestionCircle />
      </button>
      {showSources &&
        ReactDOM.createPortal(
          <div
            className="absolute z-50 min-w-max p-2 bg-white shadow-lg rounded-md border border-gray-200"
            style={{
              top: `${popupPosition.top}px`,
              left: `${popupPosition.left}px`,
            }}
          >
            {/* Display the sources list here */}
            {sourcesList}
          </div>,
          document.body // Render the popup to the body element
        )}
    </div>
  );
};
