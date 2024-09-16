import { UUID } from "crypto";

interface SortConfig<T extends object> {
  key: keyof T;
  direction: "ascending" | "descending";
}

interface HasId {
  id: number | UUID;
}

export const filterAndSort = <T extends object>(
  dataList: T[],
  searchQuery: string,
  sortConfig: SortConfig<T>,
  getComparableValue: (item: T) => string | number
): T[] => {
  let filteredList = dataList.filter((item) =>
    Object.values(item).some((value: string) =>
      value.toString().toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  if (sortConfig.key) {
    const compareStrings = (a: string | number, b: string | number) => {
      if (a < b) {
        return sortConfig.direction === "ascending" ? -1 : 1;
      }
      if (a > b) {
        return sortConfig.direction === "ascending" ? 1 : -1;
      }

      return 0;
    };

    filteredList = filteredList.sort((a, b) =>
      compareStrings(getComparableValue(a), getComparableValue(b))
    );
  }

  return filteredList;
};

export const updateSelectedItems = <T extends HasId>(params: {
  item: T;
  index: number;
  event: React.MouseEvent;
  lastSelectedIndex: number | null;
  filteredList: T[];
  selectedItems: T[];
}): { selectedItems: T[]; lastSelectedIndex: number | null } => {
  const { item, index, event, lastSelectedIndex, filteredList, selectedItems } =
    params;

  if (event.shiftKey && lastSelectedIndex !== null) {
    const start = Math.min(lastSelectedIndex, index);
    const end = Math.max(lastSelectedIndex, index);
    const range = filteredList.slice(start, end + 1);

    const newSelected = [...selectedItems];
    range.forEach((rangeItem) => {
      if (
        !newSelected.some((selectedItem) => selectedItem.id === rangeItem.id)
      ) {
        newSelected.push(rangeItem);
      }
    });

    return { selectedItems: newSelected, lastSelectedIndex: index };
  } else {
    const isSelected = selectedItems.some(
      (selectedItem) => selectedItem.id === item.id
    );
    const newSelectedItems = isSelected
      ? selectedItems.filter((selectedItem) => selectedItem.id !== item.id)
      : [...selectedItems, item];

    return {
      selectedItems: newSelectedItems,
      lastSelectedIndex: isSelected ? null : index,
    };
  }
};
