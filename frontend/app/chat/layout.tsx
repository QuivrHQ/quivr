"use client";
import { usePathname, useRouter } from "next/navigation";
import { ReactNode, useEffect } from "react";

import { KnowledgeToFeedProvider } from "@/lib/context";

interface LayoutProps {
  children?: ReactNode;
}

const Layout = ({ children }: LayoutProps): JSX.Element => {
  const pathname = usePathname();
  const router = useRouter();

  useEffect(() => {
     if (pathname === '/chat') {
      router.push('/search');
    }
  }, [pathname, router]);


  return (
    <KnowledgeToFeedProvider>
      <div className="relative h-full w-full flex justify-stretch items-stretch overflow-auto">
        {children}
      </div>
    </KnowledgeToFeedProvider>
  );
};

export default Layout;
