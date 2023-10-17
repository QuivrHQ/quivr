import Link from "next/link";
import { useTranslation } from "react-i18next";
import { LuChevronRight } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";

export const IntroSection = (): JSX.Element => {
  const { t } = useTranslation("home", { keyPrefix: "intro" });

  return (
    <>
      <div className="flex flex-col lg:flex-row items-center justify-center md:justify-start gap-10 lg:h-[calc(100vh-300px)] mb-[calc(50vw*tan(6deg))] md:mb-0">
        <div className="w-[80vw] lg:w-[60%] lg:shrink-0 flex flex-col justify-center gap-20">
          <div>
            <h1 className="text-5xl leading-[4rem] sm:text-7xl sm:leading-[6rem] font-bold text-black block max-w-2xl">
              {t("title")} <span className="text-primary">Quivr</span>
            </h1>
            <br />
            <p className="text-xl">{t("subtitle")}</p>
          </div>
          <div className="flex flex-col items-start sm:flex-row sm:items-center gap-5">
            <Link href="/signup">
              <Button className="text-white bg-black rounded-full">
                {t("try_demo")} <LuChevronRight size={24} />
              </Button>
            </Link>
            <Button variant="tertiary" className="font-semibold">
              {t("contact_sales")} <LuChevronRight size={24} />
            </Button>
          </div>
        </div>
        <div className="w-[80vw] lg:w-[calc(50vw-10%-4rem)] lg:shrink-0 h-[80vw] lg:h-[400px] bg-slate-200 rounded flex flex-col items-center justify-center">
          <p>💻 📱 Laptop / mobile image</p>
          <div className="mx-auto my-5 p-5 w-min-content bg-yellow-100 rounded-lg">
            🚧 New homepage in progress 🚧
          </div>
        </div>
      </div>
    </>
  );
};
