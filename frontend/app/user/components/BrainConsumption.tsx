import { GiBrain } from "react-icons/gi";
import { UserStats } from "../types";

export const BrainConsumption = (userStats: UserStats): JSX.Element => {
  const { current_brain_size, max_brain_size } = userStats;
  const brainFilling = current_brain_size / max_brain_size;

  const backgroundIcon = (
    <GiBrain
      style={{
        position: "absolute",
        width: "100%",
        height: "100%",
        stroke: "black",
      }}
      color="grey"
      size={12}
    />
  );

  const fillingIcon = (
    <GiBrain
      style={{
        position: "absolute",
        width: "100%",
        height: "100%",

        clipPath: `inset(${(1 - brainFilling) * 100}% 0 0 0)`,
        stroke: "black",
      }}
      color="#FF69B4"
      stroke="black"
    />
  );
  return (
    <div
      style={{
        position: "relative",
        width: "100px", // Set a width
        height: "100px", // Set a height
      }}
    >
      {backgroundIcon}
      {fillingIcon}
    </div>
  );
};
