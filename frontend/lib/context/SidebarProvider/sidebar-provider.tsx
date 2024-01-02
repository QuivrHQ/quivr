import { createContext, useEffect, useState } from "react";

import { useDevice } from "@/lib/hooks/useDevice";

type SideBarContextType = {
  isOpened: boolean;
  setIsOpened: React.Dispatch<React.SetStateAction<boolean>>;
};

export const SideBarContext = createContext<SideBarContextType | undefined>(
  undefined
);

export const SideBarProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const { isMobile } = useDevice();
  const [isOpened, setIsOpened] = useState(!isMobile);

  useEffect(() => {
    setIsOpened(!isMobile);
  }, [isMobile]);

  return (
    <SideBarContext.Provider
      value={{
        isOpened,
        setIsOpened,
      }}
    >
      {children}
    </SideBarContext.Provider>
  );
};
