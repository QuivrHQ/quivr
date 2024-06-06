import { useFromConnectionsContext } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/components/FromConnections/FromConnectionsProvider/hooks/useFromConnectionContext";
import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import QuivrButton from "@/lib/components/ui/QuivrButton/QuivrButton";

import styles from "./ConnectionButton.module.scss";

interface ConnectionButtonProps {
  label: string;
  index: number;
  onClick: (id: number) => void;
  submitted?: boolean;
  specificFiles?: boolean;
}

export const ConnectionButton = ({
  label,
  index,
  onClick,
  submitted,
  specificFiles,
}: ConnectionButtonProps): JSX.Element => {
  const { setSelectSpecificFiles } = useFromConnectionsContext();

  return (
    <div className={styles.connection_button_wrapper}>
      <div className={styles.left}>
        <ConnectionIcon letter={label[0]} index={index} />
        <span className={styles.label}>{label}</span>
      </div>
      <div className={styles.buttons_wrapper}>
        <QuivrButton
          label={submitted ? "Update" : "Use"}
          small={true}
          iconName="chevronRight"
          color="primary"
          onClick={() => {
            onClick(index);
            if (specificFiles) {
              setSelectSpecificFiles(true);
            }
          }}
        />
      </div>
    </div>
  );
};
