import { Grid, Typography } from "@mui/material";
import prettyBytes from "pretty-bytes";
import { UserStats } from "../types";

export const UserStatistics = (userStats: UserStats): JSX.Element => {
  const { email, current_brain_size, max_brain_size } = userStats;
  const brainFilling = current_brain_size / max_brain_size;

  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h6">Email: {email}</Typography>
      </Grid>
      <Grid item xs={12}>
        <Typography variant="h6">
          Brain filling: {(brainFilling * 100).toFixed(2) + "%"}
        </Typography>
        <Typography variant="h6">
          Remaining brain size:
          {prettyBytes(max_brain_size - current_brain_size, { binary: true })}
        </Typography>
      </Grid>
      <Grid item xs={12}>
        <div>
          <Typography variant="h6">Date: {userStats.date}</Typography>
        </div>
      </Grid>
    </Grid>
  );
  // );
};
