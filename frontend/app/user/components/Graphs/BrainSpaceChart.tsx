"use client";
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
  return (
    <>
      {/* @ts-expect-error Server Component */}
      <VictoryPie
        data={[
          { x: "Used", y: current_brain_size },
          { x: "Unused", y: max_brain_size - current_brain_size },
        ]}
        containerComponent={
          <VictoryContainer
            className="bg-white rounded-md w-full h-full"
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
