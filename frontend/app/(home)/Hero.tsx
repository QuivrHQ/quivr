import Link from "next/link";
import { FC } from "react";
import Button from "../components/ui/Button";
import { MdNorthEast } from "react-icons/md";

interface HeroProps {}

const Hero: FC<HeroProps> = ({}) => {
  return (
    <section className="w-full flex flex-col text-center h-screen">
      <div className="flex flex-col gap-2 items-center justify-center mt-48">
        <h1 className="mb-4 text-7xl font-bold">Get a Second Brain</h1>
        <p className="text-base max-w-sm">
          Quivr is your second brain in the cloud, designed to easily store and
          retrieve unstructured information.
        </p>
        <Link href={"/upload"}>
          <Button>Try Demo</Button>
        </Link>
        <Link target="_blank" href={"https://github.com/StanGirard/quivr/"}>
          <Button variant={"tertiary"}>
            Github <MdNorthEast />
          </Button>
        </Link>
      </div>
    </section>
  );
};

export default Hero;
