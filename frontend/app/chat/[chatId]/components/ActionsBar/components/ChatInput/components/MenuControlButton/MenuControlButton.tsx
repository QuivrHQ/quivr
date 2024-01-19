import { LuPanelLeftClose, LuPanelRightClose } from "react-icons/lu";

import styles from './MenuControlButton.module.scss'

import { useMenuContext } from "@/lib/context/MenuProvider/hooks/useMenuContext";

export const MenuControlButton = ({ visibility }: { visibility: boolean }): JSX.Element => {
    const { isOpened, setIsOpened } = useMenuContext();
    const Icon = isOpened ? LuPanelLeftClose : LuPanelRightClose;

    return (
        <div
            className={styles.menu_icon_wrapper}
            onClick={() => setIsOpened(!isOpened)}
        >
            <Icon className={styles.menu_icon} />
        </div>
    );
};
