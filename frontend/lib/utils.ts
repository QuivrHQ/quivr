import clsx, { ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export const cn = (...inputs: ClassValue[]): string => {
  return twMerge(clsx(inputs));
};

const isAdmin = (): boolean => {
  return false; // TODO change to use admin logic
}

export { isAdmin };