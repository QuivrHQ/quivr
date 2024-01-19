import { FaChevronLeft, FaChevronRight } from "react-icons/fa";

import styles from './MenuControlButton.module.scss'

import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";

export const MenuControlButton = (): JSX.Element => {
    const { isOpened, setIsOpened } = useMenuContext();
    const Icon = isOpened ? FaChevronLeft : FaChevronRight;

    return (
        <Icon
            className={styles.menu_icon}
            onClick={() => setIsOpened(!isOpened)}
        />
    );
};
