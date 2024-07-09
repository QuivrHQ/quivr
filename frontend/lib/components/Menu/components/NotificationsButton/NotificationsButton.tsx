import { MenuButton } from "@/lib/components/Menu/components/MenuButton/MenuButton";
import { useNotificationsContext } from "@/lib/context/NotificationsProvider/hooks/useNotificationsContext";

export const NotificationsButton = (): JSX.Element => {
  const { isVisible, setIsVisible } = useNotificationsContext();

  return (
    <MenuButton
      label="Notifications"
      iconName="notifications"
      type="open"
      color="primary"
      onClick={() => setIsVisible(!isVisible)}
    />
  );
};
