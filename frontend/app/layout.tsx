import { createServerComponentSupabaseClient } from "@supabase/auth-helpers-nextjs";
import { Analytics } from "@vercel/analytics/react";
import { Inter } from "next/font/google";
import { cookies, headers } from "next/headers";

//import Footer from "@/lib/components/Footer";
import { NavBar } from "@/lib/components/NavBar";
import { ToastProvider } from "@/lib/components/ui/Toast";
import { BrainProvider, FeatureFlagsProvider } from "@/lib/context";
import { BrainConfigProvider } from "@/lib/context/BrainConfigProvider/brain-config-provider";
import { SupabaseProvider } from "@/lib/context/SupabaseProvider";

import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Vantoo - 专有知识库聊天机器人",
  description:
    "专有知识库聊天机器人，可以处理各种类型文档，网页等内容，基于私有数据进行问答",
};

const RootLayout = async ({
  children,
}: {
  children: React.ReactNode;
}): Promise<JSX.Element> => {
  const supabase = createServerComponentSupabaseClient({
    headers,
    cookies,
  });

  const {
    data: { session },
  } = await supabase.auth.getSession();

  return (
    <html lang="en">
      <body
        className={`bg-white text-black min-h-screen flex flex-col dark:bg-black dark:text-white w-full ${inter.className}`}
      >
        <FeatureFlagsProvider>
        <ToastProvider>
          <SupabaseProvider session={session}>
            <BrainConfigProvider>
              <BrainProvider>
              <NavBar />
              <div className="flex-1">{children}</div>
                    {/*      <Footer /> */}
					</BrainProvider>
            </BrainConfigProvider>
          </SupabaseProvider>
        </ToastProvider>
          <Analytics />
        </FeatureFlagsProvider>
      </body>
    </html>
  );
};

export default RootLayout;
