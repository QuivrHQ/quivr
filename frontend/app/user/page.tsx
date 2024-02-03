"use client";

import { useState } from "react";

import { useSupabase } from "@/lib/context/SupabaseProvider";
import { useUserData } from "@/lib/hooks/useUserData";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { BrainsUsage } from "./components/BrainsUsage/BrainsUsage";
import { Plan } from "./components/Plan/Plan";
import { Settings } from "./components/Settings/Settings";
import { UserMenuCard } from "./components/UserMenuCard/UserMenuCard";
import { UserMenuCardProps } from "./components/types/types";
import styles from "./page.module.scss";

const UserPage = (): JSX.Element => {
  const { session } = useSupabase();
  const { userData } = useUserData();

  const [userMenuCards, setUserMenuCards] = useState<UserMenuCardProps[]>([
    {
      title: "Settings",
      subtitle: "Change your settings",
      iconName: "settings",
      selected: true,
    },
    {
      title: "Brain Usage",
      subtitle: "View your brain usage",
      iconName: "graph",
      selected: false,
    },
    {
      title: "Plan",
      subtitle: "Manage your plan",
      iconName: "unlock",
      selected: false,
    },
  ]);

  const handleCardClick = (index: number) => {
    setUserMenuCards(
      userMenuCards.map((card, i) => ({
        ...card,
        selected: i === index,
      }))
    );
  };

  if (!session || !userData) {
    redirectToLogin();
  }

  return (
    <>
      <main className={styles.user_page_container}>
        <div className={styles.left_menu_wrapper}>
          {userMenuCards.map((card, index) => (
            <UserMenuCard
              key={index}
              title={card.title}
              subtitle={card.subtitle}
              iconName={card.iconName}
              selected={card.selected}
              onClick={() => handleCardClick(index)}
            />
          ))}
        </div>
        <div className={styles.content_wrapper}>
          {userMenuCards[0].selected && <Settings email={userData.email} />}
          {userMenuCards[1].selected && <BrainsUsage />}
          {userMenuCards[2].selected && <Plan />}
        </div>
      </main>
      {/* <main className="container lg:w-2/3 mx-auto py-10 px-5">
        <Card className="mb-5 shadow-sm hover:shadow-none">

          <CardBody className="flex flex-col items-stretch max-w-max gap-2">

              <LogoutModal />
            </div>
          </CardBody>
        </Card>
        <Card className="mb-5 shadow-sm hover:shadow-none">
          <CardHeader>
            <h2 className="font-bold text-xl">
              {t("settings", { ns: "config" })}
            </h2>
          </CardHeader>

          <CardBody>
            <LanguageSelect />
          </CardBody>
        </Card>
        <Card className="mb-5 shadow-sm hover:shadow-none">
          <CardHeader>
            <h2 className="font-bold text-xl">
              {t("brainUsage", { ns: "user" })}
            </h2>
          </CardHeader>

          <CardBody>
            <UserStatistics />
          </CardBody>
        </Card>
        <Card className="mb-5 shadow-sm hover:shadow-none">
          <CardHeader>
            <h2 className="font-bold text-xl">
              {t("apiKey", { ns: "config" })}
            </h2>
          </CardHeader>

          <CardBody className="p-3 flex flex-col">
            <ApiKeyConfig />
          </CardBody>
        </Card>
      </main> */}
    </>
  );
};

export default UserPage;
