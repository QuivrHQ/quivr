import { UUID } from "crypto";

interface SortConfig<T extends object> {
  key: keyof T;
  direction: "ascending" | "descending";
}

interface HasId {
  id: number | UUID;
}

const getAllValues = <T>(obj: T): string[] => {
  let values: string[] = [];
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      const value = (obj as Record<string, unknown>)[key];
      if (typeof value === "string" || typeof value === "number") {
        values.push(value.toString());
      } else if (Array.isArray(value)) {
        values = values.concat(value.map((v: string) => v.toString()));
      } else if (typeof value === "object" && value !== null) {
        values = values.concat(getAllValues(value));
      }
    }
  }

  return values;
};

export const filterAndSort = <T extends object>(
  dataList: T[],
  searchQuery: string,
  sortConfig: SortConfig<T>,
  getComparableValue: (item: T) => unknown
): T[] => {
  let filteredList = dataList.filter((item) =>
    getAllValues(item).some((value) =>
      value.toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  const compareValues = (
    a: string | number,
    b: string | number,
    direction: "ascending" | "descending"
  ) => {
    if (a < b) {
      return direction === "ascending" ? -1 : 1;
    }
    if (a > b) {
      return direction === "ascending" ? 1 : -1;
    }

    return 0;
  };

  // Appliquer les configurations de tri
  if (sortConfig.key) {
    filteredList = filteredList.sort((a, b) => {
      const aValue = getComparableValue(a);
      const bValue = getComparableValue(b);

      // Vérifier que les valeurs sont des chaînes ou des nombres
      if (
        (typeof aValue === "string" || typeof aValue === "number") &&
        (typeof bValue === "string" || typeof bValue === "number")
      ) {
        return compareValues(aValue, bValue, sortConfig.direction);
      }

      return 0;
    });
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
