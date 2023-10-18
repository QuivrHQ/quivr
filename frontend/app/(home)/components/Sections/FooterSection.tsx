import Link from "next/link";
import { useTranslation } from "react-i18next";
import { LuChevronRight } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";

export const FooterSection = (): JSX.Element => {
  const { t } = useTranslation("home", { keyPrefix: "footer" });

  return (
    <div className="flex flex-col items-center gap-10 text-white text-center text-lg">
      <h2 className="text-3xl">{t("title")}</h2>
      <p>
        {t("description_1")} <br /> {t("description_2")}{" "}
      </p>
      <div className="flex items-center">
        <Link href="/signup">
          <Button className=" rounded-full">
            {t("start_using")}
            <LuChevronRight size={24} />
          </Button>
        </Link>
        <Button variant="tertiary">
          {t("contact_sales")} <LuChevronRight size={24} />
        </Button>
      </div>
    </div>
  );
};
