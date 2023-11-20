import Image from "next/image";
import Link from "next/link";
import { useTranslation } from "react-i18next";
import { FaGithub } from "react-icons/fa";
import { LuChevronRight } from "react-icons/lu";
import { RiTwitterXLine } from "react-icons/ri";

import Button from "@/lib/components/ui/Button";
import { GETTR_URL, GITHUB_URL, TWITTER_URL } from "@/lib/config/CONSTANTS";

import { useHomepageTracking } from "../../hooks/useHomepageTracking";

export const FooterSection = (): JSX.Element => {
  // const { t } = useTranslation("home", { keyPrefix: "footer" });
  const { t } = useTranslation(["home", "vaccineTruth"]);
  const { onLinkClick } = useHomepageTracking();

  return (
    <div className="flex flex-col items-center gap-5 text-white text-center text-lg">
      <h2 className="text-3xl">{t("footer.title", { ns: "home" })}</h2>
      <p>
        {t("footer.description_1", { ns: "home" })} <br />
        {/* {t("footer.description_2", { ns: "home" })} */}
      </p>
      <div className="flex items-center justify-center gap-2 flex-wrap">
        <Link
          href="/login"
          className="hidden"
          onClick={(event) => {
            onLinkClick({
              href: "/login",
              label: "SIGN_IN",
              event,
            });
          }}
        >
          <Button className=" rounded-full">
            {t("talkToAI", { ns: "vaccineTruth" })}
            <LuChevronRight size={24} />
          </Button>
        </Link>
        <Link
          href="/contact"
          className="hidden"
          onClick={(event) => {
            onLinkClick({
              href: "/contact",
              label: "CONTACT",
              event,
            });
          }}
        >
          <Button variant="tertiary">
            {t("intro.contact_sales", { ns: "home" })}{" "}
            <LuChevronRight size={24} />
          </Button>
        </Link>
      </div>
      <ul className="flex gap-4 mt-3 mb-6 text-black">
        <li>
          <Link href={GETTR_URL} target="_blank">
            <Image
              src={"/gettr.svg"}
              height={24}
              width={24}
              alt={"gettr icon"}
              className="hover:text-black w-12 h-12"
            ></Image>
          </Link>
        </li>
        <li>
          <a
            href={TWITTER_URL}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Quivr Twitter"
            className="hover:text-black"
          >
            <RiTwitterXLine size={52} />
          </a>
        </li>
        <li>
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Quivr GitHub"
            className="hover:text-black"
          >
            <FaGithub size={52} />
          </a>
        </li>
      </ul>
    </div>
  );
};
