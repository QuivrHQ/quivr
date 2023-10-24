import Link from "next/link";
import { useTranslation } from "react-i18next";
import { FaGithub, FaLinkedin } from "react-icons/fa";
import { LuChevronRight } from "react-icons/lu";
import { RiTwitterXLine } from "react-icons/ri";

import Button from "@/lib/components/ui/Button";
import { GITHUB_URL, LINKEDIN_URL, TWITTER_URL } from "@/lib/config/CONSTANTS";

import { useHomepageTracking } from "../../hooks/useHomepageTracking";

export const FooterSection = (): JSX.Element => {
  const { t } = useTranslation("home", { keyPrefix: "footer" });
  const { onLinkClick } = useHomepageTracking();

  return (
    <div className="flex flex-col items-center gap-10 text-white text-center text-lg">
      <h2 className="text-3xl">{t("title")}</h2>
      <p>
        {t("description_1")} <br /> {t("description_2")}{" "}
      </p>
      <div className="flex items-center justify-center gap-5 flex-wrap">
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
          <Button className=" rounded-full">
            {t("start_using")}
            <LuChevronRight size={24} />
          </Button>
        </Link>
        <Link
          href="/contact"
          onClick={(event) => {
            onLinkClick({
              href: "/contact",
              label: "CONTACT",
              event,
            });
          }}
        >
          <Button variant="tertiary">
            {t("contact_sales")} <LuChevronRight size={24} />
          </Button>
        </Link>
      </div>
      <ul className="flex gap-10 mt-5 mb-10 text-black">
        <li>
          <a
            href={LINKEDIN_URL}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Quivr LinkedIn"
            className="hover:text-black"
          >
            <FaLinkedin size={52} />
          </a>
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
