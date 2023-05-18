import { Analytics } from "@vercel/analytics/react";
import NavBar from "./components/NavBar";
import "./globals.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Quivr - Get a Second Brain with Generative AI",
  description:
    "Quivr is your second brain in the cloud, designed to easily store and retrieve unstructured information.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        className={`bg-white text-black dark:bg-black dark:text-white min-h-screen w-full ${inter.className}`}
      >
        <NavBar />
        {children}
        <Analytics />
      </body>
    </html>
  );
}
