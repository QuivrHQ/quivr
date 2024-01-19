import { GiHamburgerMenu } from "react-icons/gi";
import { LuArrowLeftFromLine } from "react-icons/lu";

import styles from './MenuControlButton.module.scss'

import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";

export const MenuControlButton = (): JSX.Element => {
    const { isOpened, setIsOpened } = useMenuContext();
    const Icon = isOpened ? LuArrowLeftFromLine : GiHamburgerMenu;

    return (
        <Icon
            className={styles.menu_icon}
            onClick={() => setIsOpened(!isOpened)}
        />
    );
};
