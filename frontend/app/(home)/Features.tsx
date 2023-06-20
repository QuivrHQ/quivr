import { ReactNode } from "react";
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
  return (
    <section className="my-20 text-center flex flex-col items-center justify-center gap-10">
      <div>
        <h1 className="text-5xl font-bold ">Features</h1>
        {/* <h2 className="opacity-50">Change the way you take notes</h2> */}
      </div>
      <div className="flex flex-wrap gap-5 justify-center">
        <Feature
          icon={<GiBrain className="text-7xl w-full" />}
          title="Two brains is better than one"
          desc="Quivr is your second brain in the cloud, designed to easily store and retrieve unstructured information."
        />
        <Feature
          icon={<GiDatabase className="text-7xl w-full" />}
          title="Store any kind of data"
          desc="Quivr can handle almost any type of data you throw at it. Text, images, code snippets, we've got you covered."
        />
        <Feature
          icon={<GiArtificialIntelligence className="text-7xl w-full" />}
          title="Get a Fast and Consistent Brain"
          desc="Quivr is your second brain in the cloud, designed to easily store and retrieve unstructured information."
        />
        <Feature
          icon={<GiFastArrow className="text-7xl w-full" />}
          title="Fast and Efficient"
          desc="Designed with speed and efficiency at its core. Quivr ensures rapid access to your data."
        />
        <Feature
          icon={<GiLockedDoor className="text-7xl w-full" />}
          title="Secure"
          desc="Your data, your control. Always."
        />
        <Feature
          icon={<GiOpenBook className="text-7xl w-full" />}
          title="Open source"
          desc="Freedom is beautiful, so is Quivr. Open source and free to use."
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
