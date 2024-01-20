"use client";
import { usePathname, useRouter } from "next/navigation";
import { ReactNode, useEffect, useState } from "react";

import { KnowledgeToFeedProvider } from "@/lib/context";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

interface LayoutProps {
  children?: ReactNode;
}

const Layout = ({ children }: LayoutProps): JSX.Element => {
  const { session } = useSupabase();
  const pathname = usePathname();
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (session === null) {
      redirectToLogin();
    } else if (pathname === '/chat') {
      router.push('/search');
    } else {
      setIsLoading(false);
    }
  }, [session, pathname, router]);

  if (isLoading) {
    return <></>
  }

  return (
    <KnowledgeToFeedProvider>
      <div className="relative h-full w-full flex justify-stretch items-stretch overflow-auto">
        {children}
      </div>
    </KnowledgeToFeedProvider>
  );
};

export default Layout;
