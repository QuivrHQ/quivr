import { useRouter } from "next/navigation";

type SidebarFooterButtonProps = {
  icon: JSX.Element;
  label: string | JSX.Element;
  href?: string;
  onClick?: () => void;
};

export const SidebarFooterButton = ({
  icon,
  label,
  href,
  onClick,
}: SidebarFooterButtonProps): JSX.Element => {
  const router = useRouter();

  if (href !== undefined) {
    onClick = () => {
      void router.push(href);
    };
  }

  return (
    <button
      type="button"
      className="w-full rounded-lg px-5 py-2 text-base flex justify-start items-center gap-4 hover:bg-gray-200 dark:hover:bg-gray-800 hover:text-primary focus:outline-none"
      onClick={onClick}
    >
      <span className="w-8 shrink-0">{icon}</span>
      <span className="w-full text-ellipsis overflow-hidden text-start">
        {label}
      </span>
    </button>
  );
};
