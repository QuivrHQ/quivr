import { Typography } from "@mui/material";
import { UserStats } from "../types";

export const DateComponent = ({ date }: UserStats): JSX.Element => {
  // Extract year, month, and day from the date string
  const year = date.slice(0, 4);
  const month = date.slice(4, 6);
  const day = date.slice(6, 8);

  const formattedDate = new Date(
    `${year}-${month}-${day}`
  ).toLocaleDateString();

  return (
    <>
      <Typography variant="h5">{"Today's date"}</Typography>
      <Typography variant="body1">{formattedDate}</Typography>
    </>
  );
};
