import { createServerComponentSupabaseClient } from "@supabase/auth-helpers-nextjs";
import { Analytics } from "@vercel/analytics/react";
import { Inter } from "next/font/google";
import { cookies, headers } from "next/headers";

import { ToastProvider } from "@/lib/components/ui/Toast";
import { BrainConfigProvider } from "@/lib/context/BrainConfigProvider";
import { BrainProvider } from "@/lib/context/BrainProvider";
import { SupabaseProvider } from "@/lib/context/SupabaseProvider";

import { App } from "./App";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Quivr - Get a Second Brain with Generative AI",
  description:
    "Quivr is your second brain in the cloud, designed to easily store and retrieve unstructured information.",
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
        <ToastProvider>
          <SupabaseProvider session={session}>
            <BrainConfigProvider>
              <BrainProvider>
                <App>
                  <div className="flex-1">{children}</div>
                </App>
              </BrainProvider>
            </BrainConfigProvider>
          </SupabaseProvider>
        </ToastProvider>
        <Analytics />
      </body>
    </html>
  );
};

export default RootLayout;
