import Link from "next/link";
import { usePathname } from "next/navigation";

import Button from "@/lib/components/ui/Button";

export const AuthButtons = (): JSX.Element => {
  const pathname = usePathname();

  if (pathname === "/signup") {
    return (
      <Link href={"/login"}>
        <Button variant={"secondary"}>Login</Button>
      </Link>
    );
  }

  return (
    <Link href={"/signup"}>
      <Button variant={"secondary"}>Register</Button>
    </Link>
  );
};
