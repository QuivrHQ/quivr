import Link from "next/link";
import { useTranslation } from "react-i18next";
import { LuChevronRight } from "react-icons/lu";

import Button from "@/lib/components/ui/Button";

import { UseCasesListing } from "./components/UseCasesListing/UseCasesListing";
import { useHomepageTracking } from "../../hooks/useHomepageTracking";

export const UseCases = (): JSX.Element => {
  const { t } = useTranslation("home");
  const { onLinkClick } = useHomepageTracking();

  return (
    <div className="text-white w-full">
      <div className="mb-3">
        <h2 className="text-center text-3xl font-semibold mb-2">
          {t("useCases.title")}
        </h2>
        <p className="text-center text-lg">{t("useCases.subtitle")}</p>
      </div>
      <UseCasesListing />
      <div className="mt-10 flex md:justify-center">
        <Link
          href="/signup"
          onClick={(event) => {
            onLinkClick({
              href: "/signup",
              label: "SIGN_UP",
              event,
            });
          }}
        >
          <Button className="bg-black rounded-full">
            {t("intro.try_demo")} <LuChevronRight size={24} />
          </Button>
        </Link>
      </div>
    </div>
  );
};
