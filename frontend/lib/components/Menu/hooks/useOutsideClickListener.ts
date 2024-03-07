import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";
import { useDevice } from "@/lib/hooks/useDevice";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useOutsideClickListener = () => {
  const { isOpened, setIsOpened } = useMenuContext();
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
