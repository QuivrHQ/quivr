import { HTMLAttributes } from "react";

import { UserStats } from "../../../lib/types/User";

interface DateComponentProps extends HTMLAttributes<HTMLSpanElement> {
  date: UserStats["date"];
}

export const DateComponent = ({
  date,
  ...props
}: DateComponentProps): JSX.Element => {
  // Extract year, month, and day from the date string
  const year = date.slice(0, 4);
  const month = date.slice(4, 6);
  const day = date.slice(6, 8);

  const formattedDate = new Date(
    `${year}-${month}-${day}`
  ).toLocaleDateString();

  return <span {...props}>{formattedDate}</span>;
};
