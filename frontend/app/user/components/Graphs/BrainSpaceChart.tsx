/* eslint-disable */
"use client";
import { useTranslation } from "react-i18next";
import {
  VictoryContainer,
  VictoryPie,
  VictoryPieProps,
  VictoryTheme,
} from "victory";

interface BrainSpaceChartProps extends VictoryPieProps {
  current_brain_size: number;
  max_brain_size: number;
}

const BrainSpaceChart = ({
  current_brain_size,
  max_brain_size,
  ...props
}: BrainSpaceChartProps): JSX.Element => {
  const { t } = useTranslation(["translation", "user"]);

  return (
    <>
      <VictoryPie
        data={[
          { x: t("Used", { ns: "user" }), y: current_brain_size },
          {
            x: t("Unused", { ns: "user" }),
            y: max_brain_size - current_brain_size,
          },
        ]}
        containerComponent={
          <VictoryContainer
            className="bg-white dark:bg-black rounded-md w-full h-full"
            responsive={true}
          />
        }
        {...props}
        theme={VictoryTheme.material}
      />
    </>
  );
};

export default BrainSpaceChart;
