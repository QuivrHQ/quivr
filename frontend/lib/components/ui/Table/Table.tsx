/* eslint-disable @typescript-eslint/no-explicit-any */
'use client';

import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  SortingState,
  useReactTable,
} from '@tanstack/react-table';
import { useState } from 'react';

import styles from './Table.module.scss';

import { Icon } from '../Icon/Icon';


interface TableProps<T> {
  data: T[];
  columns: ColumnDef<T, any>[];
  showPagination?: boolean;
  pageSize?: number;
  className?: string;
}

export const Table = <T,>({
  data,
  columns,
  showPagination = true,
  pageSize = 10,
  className = '',
}: TableProps<T>): JSX.Element => {
  const [sorting, setSorting] = useState<SortingState>([]);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    onSortingChange: setSorting,
    state: {
      sorting,
    },
    initialState: {
      pagination: {
        pageSize,
      },
    },
  });

  return (
    <div className={`${styles.table_wrapper} ${className}`}>
      <table className={styles.table}>
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map((header) => (
                <th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  className={header.column.getCanSort() ? styles.sortable : ''}
                >
                  <div className={styles.th_content}>
                    {flexRender(
                      header.column.columnDef.header,
                      header.getContext()
                    )}
                    {header.column.getIsSorted() && (
                      <span className={styles.sort_icon}>
                        {header.column.getIsSorted() === 'asc' ? (
                          <Icon name="sort" size="small" color="black" />
                        ) : (
                          <Icon name="sort" size="small" color="black" />
                        )}
                      </span>
                    )}
                  </div>
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.length > 0 ? (
            table.getRowModel().rows.map((row) => (
              <tr key={row.id}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>
                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan={columns.length}
                className={styles.empty_table}
              >
                No data available
              </td>
            </tr>
          )}
        </tbody>
      </table>

      {showPagination && data.length > 0 && (
        <div className={styles.pagination}>
          <div className={styles.pagination_info}>
            Page {table.getState().pagination.pageIndex + 1} of{' '}
            {table.getPageCount()}
          </div>
          <div className={styles.pagination_controls}>
            <button
              onClick={() => table.previousPage()}
              disabled={!table.getCanPreviousPage()}
              className={styles.pagination_button}
            >
              <Icon name="chevronLeft" size="small" color="black" />
            </button>
            <button
              onClick={() => table.nextPage()}
              disabled={!table.getCanNextPage()}
              className={styles.pagination_button}
            >
              <Icon name="chevronRight" size="small" color="black" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Table;