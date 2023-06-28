import { useContext } from "react";

import { ToastContext } from "../components/ui/Toast/domain/ToastContext";
import { ToastPublisher } from "../components/ui/Toast/domain/types";

export const useToast = (): { publish: ToastPublisher, setTop: () => void } => {
    const { publish, setTop } = useContext(ToastContext);

    const setToastOnTop = () => {
        // 在这里添加代码以将提示框设置在页面最上层
        // 将提示框的位置设置为页面布局的最上层
        const toastContainer = document.getElementById("toast-container");
        if (toastContainer) {
            toastContainer.style.zIndex = "9999";
        }
    };

    return {
        publish,
        setTop: setToastOnTop,
    };
};
