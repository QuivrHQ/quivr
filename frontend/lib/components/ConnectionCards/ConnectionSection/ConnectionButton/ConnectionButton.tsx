import { useEffect } from "react";

import { ConnectionIcon } from "@/lib/components/ui/ConnectionIcon/ConnectionIcon";
import { QuivrButton } from "@/lib/components/ui/QuivrButton/QuivrButton";
import { useSupabase } from "@/lib/context/SupabaseProvider";

import styles from "./ConnectionButton.module.scss";

interface ConnectionButtonProps {
  label: string;
  index: number;
  onClick: (id: number) => void;
  submitted?: boolean;
}

export const ConnectionButton = ({
  label,
  index,
  onClick,
  submitted,
}: ConnectionButtonProps): JSX.Element => {
  const { supabase } = useSupabase();

  useEffect(() => {
    const channel = supabase
      .channel("syncs_user")
      .on(
        "postgres_changes",
        { event: "INSERT", schema: "public", table: "syncs_user" },
        (payload) => {
          console.info("Insert event detected", payload);
        }
      )
      .on(
        "postgres_changes",
        { event: "UPDATE", schema: "public", table: "syncs_user" },
        (payload) => {
          console.info("Update event detected", payload);
        }
      )
      .on(
        "postgres_changes",
        { event: "DELETE", schema: "public", table: "syncs_user" },
        (payload) => {
          console.info("Delete event detected", payload);
        }
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
          label={submitted ? "Update" : "Use"}
          small={true}
          iconName="chevronRight"
          color="primary"
          onClick={() => onClick(index)}
        />
      </div>
    </div>
  );
};
