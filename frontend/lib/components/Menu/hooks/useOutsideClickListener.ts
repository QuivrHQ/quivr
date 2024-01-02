import { useSideBarContext } from "@/lib/context/SidebarProvider/hooks/useSideBarContext";
import { useDevice } from "@/lib/hooks/useDevice";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useOutsideClickListener = () => {
  const { isOpened, setIsOpened } = useSideBarContext();
  const { isMobile } = useDevice();

  const onClickOutside = () => {
    if (isOpened && isMobile) {
      setIsOpened(false);
    }
  };

  return {
    onClickOutside,
  };
};
