import {
  CategoryScale,
  ChartDataset,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip,
} from "chart.js";
import { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

import { useAnalytics } from "@/lib/api/analytics/useAnalyticsApi";

export const Analytics = (): JSX.Element => {
  const { getBrainsUsages } = useAnalytics();

  const [chartData, setChartData] = useState({
    labels: [] as Date[],
    datasets: [] as ChartDataset[],
  });

  useEffect(() => {
    void (async () => {
      try {
        const res = await getBrainsUsages();
        const chartLabels = res?.usages.map((usage) => usage.date) as Date[];
        const chartDataset = res?.usages.map(
          (usage) => usage.usage_count
        ) as number[];

        console.info(res?.usages);

        setChartData({
          labels: chartLabels,
          datasets: [
            {
              label: "Usage Count",
              data: chartDataset,
              borderColor: "rgb(75, 192, 192)",
              tension: 0.1,
            },
          ],
        });
      } catch (error) {
        console.error(error);
      }

      console.info(chartData);
    })();
  }, [chartData.labels.length]);

  const options = {
    scales: {
      y: {
        beginAtZero: true,
      },
    },
  };

  return (
    <div>
      <h2>Analytics</h2>
      {chartData.labels.length ? (
        <Line data={chartData} options={options} />
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};
