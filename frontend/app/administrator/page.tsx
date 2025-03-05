'use client';

// import { useRouter } from 'next/navigation';
import { useState } from 'react';

import { CreateUserModal } from '@/lib/components/CreateUserModal/CreateUserModal';
import { ListAllUsers } from '@/lib/components/ListAllUsers';
import { PageHeader } from '@/lib/components/PageHeader/PageHeader';
// import { useSupabase } from '@/lib/context/SupabaseProvider';
import { ButtonType } from '@/lib/types/QuivrButton';

import styles from './page.module.scss';

const Administrator = (): JSX.Element => {
  const [isCreateUserModalOpen, setIsCreateUserModalOpen] = useState(false);
  // const { session } = useSupabase();
  // const router = useRouter();
  // const isSuperAdmin = session?.user.role === 'super_admin';

  // useEffect(() => {
  //   if (!isSuperAdmin) {
  //     router.push('/');
  //   }
  // }, [isSuperAdmin, router]);

  const buttons: ButtonType[] = [
    {
      label: 'Create user',
      color: 'primary',
      onClick: () => {
        setIsCreateUserModalOpen(true);
      },
      iconName: 'user',
    },
  ];

  // if (!isSuperAdmin) {
  //   return <></>;
  // }

  return (
    <div className={styles.page_wrapper}>
      <div className={styles.page_header}>
        <PageHeader
          iconName='user'
          label='User Administration'
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
