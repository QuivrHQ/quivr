import {
  CategoryScale,
  ChartDataset,
  Chart as ChartJS,
  Filler,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  ScriptableContext,
  Title,
  Tooltip,
} from "chart.js";
import { useLayoutEffect, useState } from "react";
import { Line } from "react-chartjs-2";

import { formatMinimalBrainsToSelectComponentInput } from "@/app/chat/[chatId]/components/ActionsBar/components/KnowledgeToFeed/utils/formatMinimalBrainsToSelectComponentInput";
import { Range } from "@/lib/api/analytics/types";
import { useAnalytics } from "@/lib/api/analytics/useAnalyticsApi";
import { LoaderIcon } from "@/lib/components/ui/LoaderIcon/LoaderIcon";
import { MessageInfoBox } from "@/lib/components/ui/MessageInfoBox/MessageInfoBox";
import { SingleSelector } from "@/lib/components/ui/SingleSelector/SingleSelector";
import { useBrainContext } from "@/lib/context/BrainProvider/hooks/useBrainContext";
import { useDevice } from "@/lib/hooks/useDevice";

import styles from "./Analytics.module.scss";

ChartJS.register(
  CategoryScale,
  Filler,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const Analytics = (): JSX.Element => {
  const { isMobile } = useDevice();
  const { getBrainsUsages } = useAnalytics();
  const { allBrains } = useBrainContext();
  const [chartData, setChartData] = useState({
    labels: [] as Date[],
    datasets: [{}] as ChartDataset<"line", number[]>[],
  });
  const [currentChartRange, setCurrentChartRange] = useState(
    Range.WEEK as number
  );
  const [selectedBrainId, setSelectedBrainId] = useState<string | null>(null);

  const graphRangeOptions = [
    { label: "Last 7 days", value: Range.WEEK },
    { label: "Last 30 days", value: Range.MONTH },
    { label: "Last 90 days", value: Range.QUARTER },
  ];

  const brainsWithUploadRights = formatMinimalBrainsToSelectComponentInput(
    allBrains.filter((brain) => brain.brain_type === "doc")
  );

  const selectedGraphRangeOption = graphRangeOptions.find(
    (option) => option.value === currentChartRange
  );

  const handleGraphRangeChange = (newValue: number) => {
    setCurrentChartRange(newValue);
  };

  useLayoutEffect(() => {
    void (async () => {
      try {
        const res = await getBrainsUsages(selectedBrainId, currentChartRange);
        const chartLabels = res?.usages.map((usage) => usage.date) as Date[];
        const chartDataset = res?.usages.map(
          (usage) => usage.usage_count
        ) as number[];

        setChartData({
          labels: chartLabels,
          datasets: [
            {
              label: `Daily questions to ${
                selectedBrainId
                  ? allBrains.find((brain) => brain.id === selectedBrainId)
                      ?.name
                  : "your brains"
              }`,
              data: chartDataset,
              borderColor: "rgb(75, 192, 192)",
              backgroundColor: (context: ScriptableContext<"line">) => {
                const ctx = context.chart.ctx;
                const gradient = ctx.createLinearGradient(100, 100, 100, 250);
                gradient.addColorStop(0, "rgba(75, 192, 192, 0.4)");
                gradient.addColorStop(1, "rgba(75, 192, 192, 0.05)");

                return gradient;
              },
              fill: true,
              tension: 0.2,
            },
          ],
        });
      } catch (error) {
        console.error(error);
      }
    })();
  }, [chartData.labels.length, currentChartRange, selectedBrainId]);

  const options = {
    type: "line",
    scales: {
      x: {
        grid: {
          display: false,
        },
      },
      y: {
        beginAtZero: true,
        grid: {
          display: false,
        },
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return (
    <div className={styles.analytics_wrapper}>
      {!isMobile ? (
        <div>
          {chartData.labels.length ? (
            <>
              <div className={styles.selectors_wrapper}>
                <div className={styles.selector}>
                  <SingleSelector
                    iconName="calendar"
                    options={graphRangeOptions}
                    onChange={(option) => handleGraphRangeChange(option)}
                    selectedOption={selectedGraphRangeOption}
                    placeholder="Select range"
                  />
                </div>
                <div className={styles.selector}>
                  <SingleSelector
                    iconName="brain"
                    options={brainsWithUploadRights}
                    onChange={(brainId) => setSelectedBrainId(brainId)}
                    onBackClick={() => setSelectedBrainId(null)}
                    selectedOption={
                      selectedBrainId
                        ? {
                            value: selectedBrainId,
                            label: allBrains.find(
                              (brain) => brain.id === selectedBrainId
                            )?.name as string,
                          }
                        : undefined
                    }
                    placeholder="Select specific brain"
                  />
                </div>
              </div>
              <Line data={chartData} options={options} />
            </>
          ) : (
            <LoaderIcon size="big" color="accent" />
          )}
        </div>
      ) : (
        <MessageInfoBox type="warning">
          This feature is not available on small screens
        </MessageInfoBox>
      )}
    </div>
  );
};
