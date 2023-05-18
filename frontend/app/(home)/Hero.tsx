import Link from "next/link";
import { FC } from "react";
import Button from "../components/ui/Button";
import { MdNorthEast } from "react-icons/md";

interface HeroProps {}

const Hero: FC<HeroProps> = ({}) => {
  return (
    <section className="relative w-full flex flex-col gap-24 items-center text-center min-h-[768px] py-12">
      <div className="flex flex-col gap-2 items-center justify-center mt-12">
        <h1 className="text-7xl font-bold max-w-xl">
          Get a Second Brain with <span className="text-primary">Quivr</span>
        </h1>
        <p className="text-base max-w-sm text-gray-500 mb-10">
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
      <video
        className="rounded-md max-w-screen-lg shadow-lg dark:shadow-white/25 border dark:border-white/25 w-full"
        src="https://user-images.githubusercontent.com/19614572/238774100-80721777-2313-468f-b75e-09379f694653.mp4"
        autoPlay
        muted
        loop
      />
    </section>
  );
};

export default Hero;
