import Button from "@/lib/components/ui/Button";

export const DeleteOrUnsubscribeButton = (): JSX.Element => {
  if (isOwnedByCurrentUser) {
    return (
      <Button
        className="px-8 md:px-20 py-2 bg-red-500 text-white rounded-md"
        onClick={() => setIsDeleteOrUnsubscribeModalOpened(true)}
      >
        {t("deleteButton", { ns: "delete_or_unsubscribe_from_brain" })}
      </Button>
    );
  }

  return (
    <Button
      className="px-8 md:px-20 py-2 bg-red-500 text-white rounded-md"
      onClick={() => setIsDeleteOrUnsubscribeModalOpened(true)}
    >
      {t("unsubscribeButton", {
        ns: "delete_or_unsubscribe_from_brain",
      })}
    </Button>
  );
};
