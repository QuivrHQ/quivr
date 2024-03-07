import { createContext, useEffect, useState } from "react";

import { useDevice } from "@/lib/hooks/useDevice";

type MenuContextType = {
  isOpened: boolean;
  setIsOpened: React.Dispatch<React.SetStateAction<boolean>>;
};

export const MenuContext = createContext<MenuContextType | undefined>(
  undefined
);

export const MenuProvider = ({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element => {
  const { isMobile } = useDevice();
  const [isOpened, setIsOpened] = useState(false);

  useEffect(() => {
    setIsOpened(!isMobile);
  }, [isMobile]);

  return (
    <MenuContext.Provider
      value={{
        isOpened,
        setIsOpened,
      }}
    >
      {children}
    </MenuContext.Provider>
  );
};
