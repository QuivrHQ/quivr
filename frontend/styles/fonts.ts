import localFont from "next/font/local";
import { Crimson_Text, Inter } from "next/font/google";

export const cal = localFont({
  src: "./CalSans-SemiBold.otf",
  variable: "--font-display",
});

export const crimsonBold = Crimson_Text({
  weight: "700",
  variable: "--font-display",
  subsets: ["latin"],
});

export const inter = Inter({
  variable: "--font-default",
  subsets: ["latin"],
});

export const crimson = Crimson_Text({
  weight: "400",
  variable: "--font-default",
  subsets: ["latin"],
});

export const displayFontMapper = {
  "Sans Serif": cal.variable,
  Serif: crimsonBold.variable,
};

export const defaultFontMapper = {
  "Sans Serif": inter.variable,
  Serif: crimson.variable,
};
