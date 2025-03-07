import { ColumnDef } from '@tanstack/react-table';
import { format } from 'date-fns';
import { useEffect, useMemo, useState } from 'react';

import { useUserApi } from '@/lib/api/user/useUserApi';
import { UserIdentity } from '@/lib/api/user/user';
import { CreateUserModal } from '@/lib/components/CreateUserModal/CreateUserModal';
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
  const [showActionsDropdown, setShowActionsDropdown] = useState<string | null>(
    null
  );
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<UserIdentity | null>(null);
  const { getAllUsers } = useUserApi();

  const formatDate = (dateString: string | undefined): string => {
    if (!dateString) {
      return 'Never';
    }

    try {
      const date = new Date(dateString);

      if (isNaN(date.getTime())) {
        return 'Invalid date';
      }

      return format(date, 'dd MMM yyyy, h:mm:ss a');
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
          const brainNames = row.original.brain_names ?? [];
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
                  {brainNames.length > 0 ? (
                    brainNames.map((brainName, index) => (
                      <div key={index} className={styles.brains_dropdown_item}>
                        <span>{brainName}</span>
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
        cell: ({ row }) => {
          const userId = row.original.id;

          return (
            <div className={styles.actions_container}>
              <button
                className={styles.action_button}
                onClick={(e) => {
                  e.stopPropagation();
                  setShowActionsDropdown(
                    showActionsDropdown === userId ? null : userId
                  );
                }}
              >
                <Icon name='more' size='small' color='primary' />
              </button>

              {showActionsDropdown === userId && (
                <div
                  className={styles.actions_dropdown_menu}
                  onClick={(e) => e.stopPropagation()}
                >
                  <div
                    className={styles.actions_dropdown_item}
                    onClick={() => {
                      setSelectedUser(row.original);
                      setIsEditModalOpen(true);
                      setShowActionsDropdown(null);
                    }}
                  >
                    <Icon name='edit' size='small' color='primary' />
                    <span>Edit user</span>
                  </div>
                  <div className={styles.actions_dropdown_item}>
                    <Icon name='key' size='small' color='primary' />
                    <span>Reset password</span>
                  </div>
                  <div className={styles.actions_dropdown_item}>
                    <Icon name='delete' size='small' color='dangerous' />
                    <span>Deactivate user</span>
                  </div>
                </div>
              )}
            </div>
          );
        },
      },
    ],
    [showBrainsDropdown, showActionsDropdown]
  );

  // Simple function to load users data
  const loadUsers = async () => {
    try {
      setIsLoading(true);
      const fetchedUsers = await getAllUsers();
      setUsers(fetchedUsers);
      setError(null);
    } catch (err) {
      console.error('Error fetching users:', err);
      setError('Failed to load users. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  // Load users on component mount
  useEffect(() => {
    void loadUsers();
  }, []);

  // Function to manually refresh data
  const refreshData = () => {
    void loadUsers();
  };

  // Close dropdowns when clicking outside
  useEffect(() => {
    const handleClickOutside = () => {
      if (showBrainsDropdown !== null) {
        setShowBrainsDropdown(null);
      }
      if (showActionsDropdown !== null) {
        setShowActionsDropdown(null);
      }
    };

    document.addEventListener('click', handleClickOutside);

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [showBrainsDropdown, showActionsDropdown]);

  if (isLoading && users.length === 0) {
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
        <div className={styles.header_left}>
          <h2>All Users</h2>
          <p>Total users: {users.length}</p>
        </div>
        <button
          className={styles.refresh_button}
          onClick={refreshData}
          disabled={isLoading}
        >
          <Icon name='sync' size='small' color='primary' />
          {isLoading ? 'Loading...' : 'Refresh'}
        </button>
      </div>
      <Table
        data={users}
        columns={columns}
        pageSize={10}
        className={styles.users_table}
      />

      {selectedUser && (
        <CreateUserModal
          isOpen={isEditModalOpen}
          setOpen={setIsEditModalOpen}
          isEditMode={true}
          userData={selectedUser}
          onSuccess={refreshData}
        />
      )}
    </Card>
  );
};
