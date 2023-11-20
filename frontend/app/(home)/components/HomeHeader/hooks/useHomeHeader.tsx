import Link from "next/link";
import { useTranslation } from "react-i18next";
import { AiFillStar } from "react-icons/ai";
import { LuChevronRight } from "react-icons/lu";

import { useHomepageTracking } from "@/app/(home)/hooks/useHomepageTracking";
import { cn } from "@/lib/utils";

import { linkStyle } from "../styles";
import { NavbarItem } from "../types";

type UseHomeHeaderProps = {
  color: "white" | "black";
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useHomeHeader = ({ color }: UseHomeHeaderProps) => {
  const { t } = useTranslation(["home", "vaccineTruth"]);
  const { onLinkClick } = useHomepageTracking();

  const navItems: NavbarItem[] = [
    {
      href: "https://github.com/Stay-Real-Studio/vaccinetruth.ai",
      label: t("star_us"),
      leftIcon: <AiFillStar size={16} className="hidden md:inline" />,
      rightIcon: null,
    },
    { href: "/login", label: t("sign_up", { ns: "home" }) },
    { href: "/login", label: t("sign_in", { ns: "home" }) },
    {
      href: "https://www.stayreal.studio/",
      label: t("buildByStayRealStudio", { ns: "vaccineTruth" }),
      rightIcon: null,
    },
  ];

  const navLinks = (device: "mobile" | "desktop") =>
    navItems.map(
      ({ href, label, leftIcon, rightIcon, newTab = false, className }) => (
        <li key={label}>
          <Link
            href={href}
            onClick={(event) => {
              onLinkClick({
                href,
                label,
                event,
              });
            }}
            {...(newTab && { target: "_blank", rel: "noopener noreferrer" })}
            className={cn(
              "flex justify-between items-center hover:text-primary p-2 gap-1",
              device === "desktop" ? linkStyle[color] : null,
              className
            )}
          >
            {leftIcon}
            {label}
            {rightIcon !== null && (rightIcon ?? <LuChevronRight size={16} />)}
          </Link>
        </li>
      )
    );

  return {
    navLinks,
  };
};
