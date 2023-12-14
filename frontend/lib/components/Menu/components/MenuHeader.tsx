import { Logo } from "@/lib/components/Logo/Logo";

export const MenuHeader = (): JSX.Element => {
  return (
    <div className="p-2 relative">
      <div className="max-w-screen-xl flex justify-between items-center pt-3 pl-3">
        <Logo />
      </div>
    </div>
  );
};
