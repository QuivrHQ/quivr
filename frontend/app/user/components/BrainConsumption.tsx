import { useTranslation } from "react-i18next";
import { GiBrain } from "react-icons/gi";

import { UserStats } from "../../../lib/types/User";

export const BrainConsumption = (userStats: UserStats): JSX.Element => {
  const { current_brain_size, max_brain_size } = userStats;
  const brainFilling = current_brain_size / max_brain_size;
  const { t } = useTranslation(["translation","user"]);

  const backgroundIcon = (
    <GiBrain
      style={{
        position: "absolute",
        width: "100%",
        height: "100%",
      }}
      className="fill-green-200 stroke-black stroke-1"
    />
  );

  const fillingIcon = (
    <GiBrain
      style={{
        position: "absolute",
        width: "100%",
        height: "100%",
        clipPath: `inset(${(1 - brainFilling) * 100}% 0 0 0)`,
      }}
      className="fill-pink-300 stroke-black stoke-1"
    />
  );

  return (
    <div className="flex flex-col items-center justify-center w-fit">
      <div className="w-24 h-24 relative">
        {backgroundIcon}
        {fillingIcon}
      </div>
      <div className="flex flex-col items-center justify-center">
        <span className="font-semibold">
          {/* Percentage of brain space left */}
          {(100 - brainFilling * 100).toFixed(2)}%{" "}
        </span>
        <span className="text-sm opacity-50">{t("empty", {ns: "user"})}</span>
      </div>
    </div>
  );
};
