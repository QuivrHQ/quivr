import { Box, Grid, Typography } from "@mui/material";
import prettyBytes from "pretty-bytes";
import { UserStats } from "../types";
import { BrainConsumption } from "./BrainConsumption";
import { DateComponent } from "./Date";
import { RequestsPerDayChart } from "./RequestsPerDayChart";

export const UserStatistics = (userStats: UserStats): JSX.Element => {
  const { email, current_brain_size, max_brain_size } = userStats;
  const brainFilling = current_brain_size / max_brain_size;
  return (
    <Box>
      <Grid container spacing={2}>
        <Grid item xs={6}>
          <Typography variant="h6">Email</Typography>
          <Typography variant="body1">{email}</Typography>
        </Grid>
        <Grid item xs={6} style={{ textAlign: "right" }}>
          <DateComponent {...userStats} />
        </Grid>
      </Grid>
      <Grid container spacing={2}>
        <Grid item xs={8}>
          <div
            style={{
              position: "relative",
              maxWidth: "100%",
              maxHeight: "100%",
              width: "200px", // Set a width
              height: "200px", // Set a height
            }}
          >
            <RequestsPerDayChart {...userStats} />
          </div>
        </Grid>
        <Grid item xs={4}>
          <BrainConsumption {...userStats} />
          <Typography variant="h6">Brain filling</Typography>
          <Typography variant="body1">
            {(brainFilling * 100).toFixed(2) + "%"}
          </Typography>
          <Typography variant="h6">Remaining brain size</Typography>
          <Typography variant="body1">
            {prettyBytes(max_brain_size - current_brain_size, { binary: true })}
          </Typography>
        </Grid>
      </Grid>
    </Box>
  );
};
