import * as Popover from "@radix-ui/react-popover";
import { LuMenu, LuX } from "react-icons/lu";

import { QuivrLogo } from "@/lib/assets/QuivrLogo";
import { cn } from "@/lib/utils";

type PopoverMenuMobileProps = {
  navLinks: JSX.Element[];
  color?: "white" | "black";
};

export const PopoverMenuMobile = ({
  navLinks,
  color = "white",
}: PopoverMenuMobileProps): JSX.Element => {
  return (
    <>
      <Popover.Root>
        <div>
          <Popover.Anchor />
          <Popover.Trigger
            title="menu"
            type="button"
            className={cn(
              "bg-[#D9D9D9] bg-opacity-30 rounded-full px-4 py-1",
              color === "white" ? "text-white" : "text-black"
            )}
          >
            <LuMenu size={32} />
          </Popover.Trigger>
        </div>
        <Popover.Content
          style={{
            minWidth: "max-content",
            backgroundColor: "white",
            borderRadius: "0.75rem",
            paddingTop: "0.5rem",
            paddingInline: "1rem",
            paddingBottom: "1.5rem",
            marginRight: "1rem",
            marginTop: "-1rem",
            boxShadow: "0 0 0.5rem rgba(0, 0, 0, 0.1)",
          }}
        >
          <div className="flex flex-col gap-4 min-w-max w-[calc(100vw-4rem)] sm:w-[300px]">
            <div className="flex justify-between items-center">
              <div className="flex gap-2 items-center">
                <QuivrLogo size={64} color="primary" />
                <div className="text-lg font-medium text-primary cursor-default ">
                  Quivr
                </div>
              </div>
              <Popover.Close>
                <button
                  title="close"
                  type="button"
                  className="hover:text-primary p-2"
                >
                  <LuX size={24} />
                </button>
              </Popover.Close>
            </div>
            <nav>
              <ul className="flex flex-col bg-[#F5F8FF] rounded-xl p-2">
                {navLinks}
              </ul>
            </nav>
          </div>
        </Popover.Content>
      </Popover.Root>
    </>
  );
};
