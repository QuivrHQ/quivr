import Link from "next/link";
import { Dispatch, FC, ReactNode, SetStateAction } from "react";

interface NavLinkProps {
  children: ReactNode;
  to: string;
  setOpen?: Dispatch<SetStateAction<boolean>>;
}

export const NavLink: FC<NavLinkProps> = ({ children, to, setOpen }) => {
  return (
    <li className="group relative">
      <Link onClick={() => setOpen && setOpen(false)} href={to}>
        {children}
      </Link>
      <hr className="aboslute top-full border border-transparent border-b-primary dark:border-b-white scale-x-0 group-hover:scale-x-100 group-focus-within:scale-x-100 transition-transform" />
    </li>
  );
};
