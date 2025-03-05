import { ColumnDef } from '@tanstack/react-table';
import { useEffect, useMemo, useState } from 'react';

import { useUserApi } from '@/lib/api/user/useUserApi';
import { UserIdentity } from '@/lib/api/user/user';
import Card from '@/lib/components/ui/Card';
import { Icon } from '@/lib/components/ui/Icon/Icon';
import Spinner from '@/lib/components/ui/Spinner';
import Table from '@/lib/components/ui/Table/Table';

import styles from './ListAllUsers.module.scss';

export const ListAllUsers = (): JSX.Element => {
  const [users, setUsers] = useState<UserIdentity[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showBrainsDropdown, setShowBrainsDropdown] = useState<string | null>(
    null
  );
  const { getAllUsers } = useUserApi();

  const formatDate = (dateString: string | undefined): string => {
    if (!dateString) {
      return 'Never';
    }

    try {
      const date = new Date(dateString);

      return date.toLocaleString();
    } catch (e) {
      return 'Invalid date';
    }
  };

  const columns = useMemo<ColumnDef<UserIdentity>[]>(
    () => [
      {
        accessorKey: 'username',
        header: 'Name',
        cell: ({ row }) => row.original.username || 'N/A',
      },
      {
        accessorKey: 'email',
        header: 'Email',
        cell: ({ row }) => row.original.email ?? 'N/A',
      },
      {
        accessorKey: 'brains',
        header: 'Brains',
        cell: ({ row }) => {
          const brains = row.original.brains ?? [];
          const userId = row.original.id;

          return (
            <div className={styles.brains_container}>
              <div
                className={styles.brains_dropdown_trigger}
                onClick={(e) => {
                  e.stopPropagation();
                  setShowBrainsDropdown(
                    showBrainsDropdown === userId ? null : userId
                  );
                }}
              >
                {brains.length > 0
                  ? `Admin and ${brains.length} other brain${
                      brains.length > 1 ? 's' : ''
                    }`
                  : 'No brain'}{' '}
                <Icon name='chevronDown' size='small' color='primary' />
              </div>

              {showBrainsDropdown === userId && (
                <div
                  className={styles.brains_dropdown_menu}
                  onClick={(e) => e.stopPropagation()}
                >
                  <div className={styles.brains_dropdown_group_label}>
                    Brains
                  </div>

                  {brains.length > 0 ? (
                    brains.map((brain, index) => (
                      <div key={index} className={styles.brains_dropdown_item}>
                        <span>{brain}</span>
                        {index === 2 && (
                          <Icon name='check' size='small' color='success' />
                        )}
                      </div>
                    ))
                  ) : (
                    <div className={styles.brains_dropdown_item}>
                      <span>No brains assigned</span>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        },
      },
      {
        accessorKey: 'last_sign_in_at',
        header: 'Last Login',
        cell: ({ row }) => formatDate(row.original.last_sign_in_at),
      },
      {
        id: 'actions',
        header: 'Actions',
        cell: () => (
          <div className={styles.actions_container}>
            <button className={styles.action_button}>
              <Icon name='more' size='small' color='primary' />
            </button>
          </div>
        ),
      },
    ],
    [showBrainsDropdown]
  );

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        setIsLoading(true);
        const fetchedUsers = await getAllUsers();
        setUsers(fetchedUsers);
        setIsLoading(false);

        setError(null);
      } catch (err) {
        console.error('Error fetching users:', err);
        setError('Failed to load users. Please try again later.');
        setIsLoading(false);
      }
    };

    void fetchUsers();
  }, [getAllUsers]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = () => {
      if (showBrainsDropdown !== null) {
        setShowBrainsDropdown(null);
      }
    };

    document.addEventListener('click', handleClickOutside);

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [showBrainsDropdown]);

  if (isLoading) {
    return (
      <div className={styles.loading_container}>
        <Spinner />
        <p>Loading users...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.error_container}>
        <Icon name='warning' size='large' color='warning' />
        <p>{error}</p>
      </div>
    );
  }

  return (
    <Card className={styles.users_card}>
      <div className={styles.card_header}>
        <h2>All Users</h2>
        <p>Total users: {users.length}</p>
      </div>
      <Table
        data={users}
        columns={columns}
        pageSize={5}
        className={styles.users_table}
      />
    </Card>
  );
};
