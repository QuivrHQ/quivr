import { useEffect, useRef, useState } from "react";

import { DeleteOrUnsubscribeConfirmationModal } from "@/app/studio/[brainId]/BrainManagementTabs/components/DeleteOrUnsubscribeModal/DeleteOrUnsubscribeConfirmationModal";
import { useBrainFetcher } from "@/app/studio/[brainId]/BrainManagementTabs/hooks/useBrainFetcher";
import { useBrainManagementTabs } from "@/app/studio/[brainId]/BrainManagementTabs/hooks/useBrainManagementTabs";
import { getBrainPermissions } from "@/app/studio/[brainId]/BrainManagementTabs/utils/getBrainPermissions";
import { Icon } from "@/lib/components/ui/Icon/Icon";
import { OptionsModal } from "@/lib/components/ui/OptionsModal/OptionsModal";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { MinimalBrainForUser } from "@/lib/context/BrainProvider/types";
import { useSearchModalContext } from "@/lib/context/SearchModalProvider/hooks/useSearchModalContext";
import { useUserSettingsContext } from "@/lib/context/UserSettingsProvider/hooks/useUserSettingsContext";
import { Option } from "@/lib/types/Options";

import styles from "./BrainItem.module.scss";

type BrainItemProps = {
  brain: MinimalBrainForUser;
  even: boolean;
};

export const BrainItem = ({ brain, even }: BrainItemProps): JSX.Element => {
  const [optionsOpened, setOptionsOpened] = useState<boolean>(false);
  const [optionsHovered, setOptionsHovered] = useState<boolean>(false);

  const {
    handleUnsubscribeOrDeleteBrain,
    isDeleteOrUnsubscribeModalOpened,
    setIsDeleteOrUnsubscribeModalOpened,
    isDeleteOrUnsubscribeRequestPending,
  } = useBrainManagementTabs(brain.id);
  const { allBrains, setCurrentBrainId } = useBrainContext();
  const { isOwnedByCurrentUser } = getBrainPermissions({
    brainId: brain.id,
    userAccessibleBrains: allBrains,
  });
  const { brain: fetchedBrain } = useBrainFetcher({ brainId: brain.id });
  const { isDarkMode } = useUserSettingsContext();
  const { setIsVisible } = useSearchModalContext();

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
      label: "Talk to Brain",
      onClick: () => {
        setOptionsOpened(false);
        setIsVisible(true);
        setTimeout(() => setCurrentBrainId(brain.id));
      },
      iconName: "chat",
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
      <a
        className={`
      ${even ? styles.even : styles.odd}
      ${styles.brain_item_wrapper} ${optionsHovered ? styles.not_hovered : ""}
      `}
        href={`/studio/${brain.id}`}
      >
        <div className={styles.brain_header}>
          <div className={styles.left}>
            <div
              className={styles.brain_snippet}
              style={{ backgroundColor: brain.snippet_color }}
            >
              <span>{brain.snippet_emoji}</span>
            </div>
            <span className={styles.name}>{brain.name}</span>
          </div>
          <div
            ref={iconRef}
            onClick={(event: React.MouseEvent<HTMLElement>) => {
              event.nativeEvent.stopImmediatePropagation();
              event.stopPropagation();
              event.preventDefault();
              setOptionsOpened(!optionsOpened);
            }}
            className={styles.icon}
          >
            <div
              onMouseEnter={() => setOptionsHovered(true)}
              onMouseLeave={() => setOptionsHovered(false)}
            >
              <Icon
                name="options"
                size="small"
                color="black"
                handleHover={true}
              />
            </div>
          </div>
        </div>
        <div className={styles.model}>
          <span className={styles.title}>Model:</span>
          <span className={styles.model_type}>
            {fetchedBrain?.model ?? "gpt-3.5-turbo-0125"}
          </span>
        </div>

        <span className={styles.description}>{brain.description}</span>
        <div>
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
        <div
          ref={optionsRef}
          className={styles.options_modal}
          onMouseEnter={() => setOptionsHovered(true)}
          onMouseLeave={() => setOptionsHovered(false)}
        >
          {optionsOpened && <OptionsModal options={options} />}
        </div>
      </a>
    </>
  );
};
