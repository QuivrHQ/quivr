import Image from "next/image";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import { DeleteOrUnsubscribeConfirmationModal } from "@/app/studio/[brainId]/BrainManagementTabs/components/DeleteOrUnsubscribeModal/DeleteOrUnsubscribeConfirmationModal";
import { useBrainManagementTabs } from "@/app/studio/[brainId]/BrainManagementTabs/hooks/useBrainManagementTabs";
import { getBrainPermissions } from "@/app/studio/[brainId]/BrainManagementTabs/utils/getBrainPermissions";
import Icon from "@/lib/components/ui/Icon/Icon";
import { OptionsModal } from "@/lib/components/ui/OptionsModal/OptionsModal";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { Option } from "@/lib/types/Options";

import styles from "./BrainItem.module.scss";

type BrainItemProps = {
  brain: MinimalBrainForUser;
  even: boolean;
};

export const BrainItem = ({ brain, even }: BrainItemProps): JSX.Element => {
  const [optionsOpened, setOptionsOpened] = useState<boolean>(false);

  const {
    handleUnsubscribeOrDeleteBrain,
    isDeleteOrUnsubscribeModalOpened,
    setIsDeleteOrUnsubscribeModalOpened,
    isDeleteOrUnsubscribeRequestPending,
  } = useBrainManagementTabs(brain.id);
  const { allBrains } = useBrainContext();
  const { isOwnedByCurrentUser } = getBrainPermissions({
    brainId: brain.id,
    userAccessibleBrains: allBrains,
  });
  const { isDarkMode } = useUserSettingsContext();

  const iconRef = useRef<HTMLDivElement | null>(null);
  const optionsRef = useRef<HTMLDivElement | null>(null);

  const options: Option[] = [
    {
      label: "Edit",
      onClick: () => (window.location.href = `/studio/${brain.id}`),
      iconName: "edit",
      iconColor: "primary",
    },
    {
      label: "Delete",
      onClick: () => void setIsDeleteOrUnsubscribeModalOpened(true),
      iconName: "delete",
      iconColor: "dangerous",
    },
  ];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        iconRef.current &&
        !iconRef.current.contains(event.target as Node) &&
        optionsRef.current &&
        !optionsRef.current.contains(event.target as Node)
      ) {
        setOptionsOpened(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isDarkMode]);

  return (
    <>
      <div
        className={`
      ${even ? styles.even : styles.odd}
      ${styles.brain_item_wrapper}
      `}
      >
        <Image
          className={isDarkMode ? styles.dark_image : ""}
          src={
            brain.integration_logo_url
              ? brain.integration_logo_url
              : "/default_brain_image.png"
          }
          alt="logo_image"
          width={18}
          height={18}
        />

        <Link
          className={styles.brain_info_wrapper}
          href={`/studio/${brain.id}`}
        >
          <span className={styles.name}>{brain.name}</span>
          <span className={styles.description}>{brain.description}</span>
        </Link>
        <div>
          <div
            ref={iconRef}
            onClick={(event: React.MouseEvent<HTMLElement>) => {
              event.nativeEvent.stopImmediatePropagation();
              setOptionsOpened(!optionsOpened);
            }}
          >
            <Icon
              name="options"
              size="normal"
              color="black"
              handleHover={true}
            />
          </div>
          <DeleteOrUnsubscribeConfirmationModal
            isOpen={isDeleteOrUnsubscribeModalOpened}
            setOpen={setIsDeleteOrUnsubscribeModalOpened}
            onConfirm={() => void handleUnsubscribeOrDeleteBrain()}
            isOwnedByCurrentUser={isOwnedByCurrentUser}
            isDeleteOrUnsubscribeRequestPending={
              isDeleteOrUnsubscribeRequestPending
            }
          />
        </div>
        <div ref={optionsRef} className={styles.options_modal}>
          {optionsOpened && <OptionsModal options={options} />}
        </div>
      </div>
    </>
  );
};
