import { GiHamburgerMenu } from "react-icons/gi";
import { LuArrowLeftFromLine } from "react-icons/lu";

import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";
import { useDevice } from "@/lib/hooks/useDevice";

import styles from './MenuControlButton.module.scss';

export const MenuControlButton = (): JSX.Element => {
    const { isOpened, setIsOpened } = useMenuContext();
    const { isMobile } = useDevice();
    const Icon = isOpened ? LuArrowLeftFromLine : GiHamburgerMenu;

    if (isOpened && isMobile) {
        return <></>;
    }

    return (
        <Icon
            className={styles.menu_icon}
            onClick={() => setIsOpened(!isOpened)}
        />
    );
};
