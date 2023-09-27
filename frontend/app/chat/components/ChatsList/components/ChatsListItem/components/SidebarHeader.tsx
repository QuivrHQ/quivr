import { Logo } from "@/lib/components/NavBar/components/Logo";

export const SidebarHeader = (): JSX.Element => {
  return (
    <div className="border-b dark:border-white/10 p-2">
      <div className="max-w-screen-xl flex justify-center items-center flex-col pt-3">
        <Logo />
      </div>
    </div>
  );
};
