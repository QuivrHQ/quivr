"use client";

import { useState } from "react";
import { useTranslation } from "react-i18next";

import { CreateUserModal } from "@/lib/components/CreateUserModal/CreateUserModal";
import { ListAllUsers } from "@/lib/components/ListAllUsers";
import { PageHeader } from "@/lib/components/PageHeader/PageHeader";
import { ButtonType } from "@/lib/types/QuivrButton";

import styles from "./page.module.scss";

const Administrator = (): JSX.Element => {
  const { t } = useTranslation(["user"]);
  const [isCreateUserModalOpen, setIsCreateUserModalOpen] = useState(false);

  const buttons: ButtonType[] = [
    {
      label: t("create_user", { ns: "user" }),
      color: "primary",
      onClick: () => {
        setIsCreateUserModalOpen(true);
      },
      iconName: "user",
    },
  ];

  return (
    <div className={styles.page_wrapper}>
      <div className={styles.page_header}>
        <PageHeader
          iconName='user'
          label={t("user_administration", { ns: "user" })}
          buttons={buttons}
        />
      </div>
      <div className={styles.content_wrapper}>
        <ListAllUsers />
      </div>
      <CreateUserModal
        isOpen={isCreateUserModalOpen}
        setOpen={setIsCreateUserModalOpen}
      />
    </div>
  );
};

export default Administrator;
