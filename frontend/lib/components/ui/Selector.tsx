import { useChatContext } from '@/app/chat/[chatId]/context/ChatContext';
import React, { useState } from 'react';

type SelectorProps = {
  choice1: string;
  choice2?: string;
};

const Selector: React.FC<SelectorProps> = ({ choice1, choice2 }) => {
  const [activeChoice, setActiveChoice] = useState(choice1);
  const { setDocRetrieval } = useChatContext();

  const handleClick = (choice: string) => {
    setActiveChoice(choice);
    setDocRetrieval(choice == "Ask Brain")
  };

  return (
    <div className="flex flex-col items-center justify-center px-5">
      <div className="relative flex rounded-xl bg-gray-100 p-1 text-gray-900 dark:bg-gray-900">
        <ul className="flex w-full list-none gap-1 sm:w-auto">
          <li className="group/toggle w-full">
            <button
              type="button"
              id="radix-:ra:"
              aria-haspopup="menu"
              aria-expanded="false"
              data-state="closed"
              className={`w-full cursor-pointer ${
                activeChoice === choice1 ? 'bg-gray-300 text-white' : 'bg-white text-gray-900'
              }`}
              onClick={() => handleClick(choice1)}
            >
              <div className="group/button relative flex w-full items-center justify-center gap-1 rounded-lg border py-3 outline-none transition-opacity duration-100 sm:w-auto sm:min-w-[148px] md:gap-2 md:py-2.5 border-black/10 text-gray-900 hover:!opacity-100 dark:border-[#4E4F60] dark:bg-gray-700 dark:text-gray-100">
                <span className="relative max-[370px]:hidden">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 16 16"
                    fill="none"
                    className={`h-4 w-4 transition-colors ${
                      activeChoice === choice1 ? 'text-white' : 'text-brand-green'
                    }`}
                    width="16"
                    height="16"
                    strokeWidth="2"
                  >
                    <path
                      d="M9.586 1.526A.6.6 0 0 0 8.553 1l-6.8 7.6a.6.6 0 0 0 .447 1h5.258l-1.044 4.874A.6.6 0 0 0 7.447 15l6.8-7.6a.6.6 0 0 0-.447-1H8.542l1.044-4.874Z"
                      fill="currentColor"
                    />
                  </svg>
                </span>
                <span className="truncate text-sm font-medium md:pr-1.5 pr-1.5">
                  {choice1}
                </span>
              </div>
            </button>
          </li>
          <li className="group/toggle w-full">
            <button
              type="button"
              id="radix-:rc:"
              aria-haspopup="menu"
              aria-expanded="false"
              data-state="closed"
              className={`w-full cursor-pointer ${
                activeChoice === choice2 ? 'bg-gray-300 text-white' : 'bg-white text-gray-900'
              }`}
              onClick={() => handleClick(choice2 || '')}
            >
              <div className="group/button relative flex w-full items-center justify-center gap-1 rounded-lg border py-3 outline-none transition-opacity duration-100 sm:w-auto sm:min-w-[148px] md:gap-2 md:py-2.5 border-transparent text-gray-500 hover:text-gray-800 hover:dark:text-gray-100">
                <span className="relative max-[370px]:hidden">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 16 16"
                    fill="none"
                    className={`h-4 w-4 transition-colors group-hover/button:text-brand-purple ${
                      activeChoice === choice2 ? 'text-white' : 'text-brand-purple'
                    }`}
                    width="16"
                    height="16"
                    strokeWidth="2"
                  >
                    <path
                      d="M12.784 1.442a.8.8 0 0 0-1.569 0l-.191.953a.8.8 0 0 1-.628.628l-.953.19a.8.8 0 0 0 0 1.57l.953.19a.8.8 0 0 1 .628.629l.19.953a.8.8 0 0 0 1.57 0l.19-.953a.8.8 0 0 1 .629-.628l.953-.19a.8.8 0 0 0 0-1.57l-.953-.19a.8.8 0 0 1-.628-.629l-.19-.953h-.002ZM5.559 4.546a.8.8 0 0 0-1.519 0l-.546 1.64a.8.8 0 0 1-.507.507l-1.64.546a.8.8 0 0 0 0 1.519l1.64.547a.8.8 0 0 1 .507.505l.546 1.641a.8.8 0 0 0 1.519 0l.546-1.64a.8.8 0 0 1 .506-.507l1.641-.546a.8.8 0 0 0 0-1.519l-1.64-.546a.8.8 0 0 1-.507-.506L5.56 4.546Zm5.6 6.4a.8.8 0 0 0-1.519 0l-.147.44a.8.8 0 0 1-.505.507l-.441.146a.8.8 0 0 0 0 1.519l.44.146a.8.8 0 0 1 .507.506l.146.441a.8.8 0 0 0 1.519 0l.147-.44a.8.8 0 0 1 .506-.507l.44-.146a.8.8 0 0 0 0-1.519l-.44-.147a.8.8 0 0 1-.507-.505l-.146-.441Z"
                      fill="currentColor"
                    />
                  </svg>
                </span>
                <span className="truncate text-sm font-medium md:pr-1.5 pr-1.5">
                  {choice2}
                </span>
              </div>
            </button>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default Selector;
