"use client";
import { ReactNode } from "react";
import { useTranslation } from "react-i18next";
import {
  GiArtificialIntelligence,
  GiBrain,
  GiDatabase,
  GiFastArrow,
  GiLockedDoor,
  GiOpenBook,
} from "react-icons/gi";

import Card from "@/lib/components/ui/Card";

const Features = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <section className="my-20 text-center flex flex-col items-center justify-center gap-10">
      <div>
        <h1 className="text-5xl font-bold ">{t("features")}</h1>
        {/* <h2 className="opacity-50">Change the way you take notes</h2> */}
      </div>
      <div className="flex flex-wrap gap-5 justify-center">
        <Feature
          icon={<GiBrain className="text-7xl w-full" />}
          title={t("two_brains_title")}
          desc={t("two_brains_desc")}
        />
        <Feature
          icon={<GiDatabase className="text-7xl w-full" />}
          title={t("any_kind_of_data_title")}
          desc={t("any_kind_of_data_desc")}
        />
        <Feature
          icon={<GiArtificialIntelligence className="text-7xl w-full" />}
          title={t("fast_and_accurate_title")} 
          desc={t("fast_and_accurate_desc")}
        />
        <Feature
          icon={<GiFastArrow className="text-7xl w-full" />}
          title={t("fast_and_efficient_title")}
          desc={t("fast_and_efficient_desc")}
        />
        <Feature
          icon={<GiLockedDoor className="text-7xl w-full" />}
          title={t("secure_title")}
          desc={t("secure_desc")}
        />
        <Feature
          icon={<GiOpenBook className="text-7xl w-full" />}
          title={t("open_source_title")}
          desc={t("open_source_desc")}
        />
      </div>
    </section>
  );
};

interface FeatureProps {
  icon?: ReactNode;
  title: string;
  desc: string;
}

const Feature = ({ title, desc, icon }: FeatureProps): JSX.Element => {
  return (
    <Card className="p-10 max-w-xs flex flex-col gap-5 w-full">
      {icon}
      <h1 className="text-xl font-bold">{title}</h1>
      <p>{desc}</p>
    </Card>
  );
};

export default Features;
