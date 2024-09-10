import { useEffect, useState } from "react";

import { Sync, SyncStatus } from "@/lib/api/sync/types";
import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import styles from "./ConnectionButton.module.scss";

interface ConnectionButtonProps {
  label: string;
  index: number;
  onClick: (id: number) => void;
  submitted?: boolean;
  sync: Sync;
}

export const ConnectionButton = ({
  label,
  index,
  onClick,
  submitted,
  sync,
}: ConnectionButtonProps): JSX.Element => {
  const { supabase } = useSupabase();
  const [status, setStatus] = useState<SyncStatus>(sync.status);

  const handleStatusChange = (payload: { new: Sync }) => {
    if (payload.new.id === sync.id) {
      setStatus(payload.new.status);
    }
  };

  useEffect(() => {
    setStatus(sync.status);
    const channel = supabase
      .channel("syncs_user")
      .on(
        "postgres_changes",
        { event: "UPDATE", schema: "public", table: "syncs_user" },
        handleStatusChange
      )
      .subscribe();

    return () => {
      void supabase.removeChannel(channel);
    };
  }, []);

  return (
    <div className={styles.connection_button_wrapper}>
      <div className={styles.left}>
        <ConnectionIcon letter={label[0]} index={index} />
        <span className={styles.label}>{label}</span>
      </div>
      <div className={styles.buttons_wrapper}>
        <QuivrButton
          label={
            submitted ? "Update" : status === "SYNCED" ? "Use" : "Syncing..."
          }
          small={true}
          iconName="chevronRight"
          color="primary"
          onClick={() => onClick(index)}
          disabled={status === "SYNCING"}
        />
      </div>
    </div>
  );
};
