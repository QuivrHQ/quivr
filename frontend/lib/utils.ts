import clsx, { ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export const cn = (...inputs: ClassValue[]): string => {
  return twMerge(clsx(inputs));
};


const isToday = (date: Date): boolean => {
  const today = new Date();

  return date.toDateString() === today.toDateString();
};

const isYesterday = (date: Date): boolean => {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);

  return date.toDateString() === yesterday.toDateString();
};

const isWithinLast7Days = (date: Date): boolean => {
  const weekAgo = new Date();
  weekAgo.setDate(weekAgo.getDate() - 7);

  return date > weekAgo && !isToday(date) && !isYesterday(date);
};

const isWithinLast30Days = (date: Date): boolean => {
  const monthAgo = new Date();
  monthAgo.setDate(monthAgo.getDate() - 30);

  return date > monthAgo && !isToday(date) && !isYesterday(date) && !isWithinLast7Days(date);
};

export { isToday, isWithinLast30Days, isWithinLast7Days, isYesterday };
