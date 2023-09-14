import { useTranslation } from "react-i18next";
import { MdKeyboardCommandKey } from "react-icons/md";

import { ShortcutItem } from "./components";

export const ShortCuts = (): JSX.Element => {
  const { t } = useTranslation(["chat"]);

  const shortcuts = [
    {
      content: [t("shortcut_select_brain"), t("shortcut_choose_prompt")],
    },
    // {
    //   content: [
    //     t("shortcut_select_file"),
    //     t("shortcut_create_brain"),
    //     t("shortcut_feed_brain"),
    //     t("shortcut_create_prompt"),
    //   ],
    // },
    // {
    //   content: [
    //     t("shortcut_manage_brains"),
    //     t("shortcut_go_to_user_page"),
    //     t("shortcut_go_to_shortcuts"),
    //   ],
    // },
  ];

  return (
    <>
      <div className="flex items-center justify-center">
        <MdKeyboardCommandKey className="text-4xl mr-2" />
        <span className="font-bold text-2xl">{t("keyboard_shortcuts")}</span>
      </div>
      <div className="flex-1 flex items-center justify-center">
        <div className="flex flex-row space-x-4">
          {shortcuts.map((shortcut, index) => (
            <ShortcutItem key={index} content={shortcut.content} />
          ))}
        </div>
      </div>
    </>
  );
};
