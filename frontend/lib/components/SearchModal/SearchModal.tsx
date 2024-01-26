import { useEffect, useRef, useState } from "react";

import styles from "./SearchModal.module.scss";

import { SearchBar } from "../ui/SearchBar/SearchBar";

export const SearchModal = (): JSX.Element => {
  const [isVisible, setIsVisible] = useState(false);
  const searchBarRef = useRef(null);
  const searchBarClassName = "SearchModal_search_modal_wrapper";

  const keydownHandler = ({
    key,
    metaKey,
  }: {
    key: string;
    metaKey: boolean;
  }) => {
    if (metaKey && key === "k") {
      setIsVisible(true);
    }
  };

  const mousedownHandler = (event: MouseEvent) => {
    if (
      event.target instanceof HTMLElement &&
      event.target.className !== searchBarClassName
    ) {
      setIsVisible(false);
    }
  };

  useEffect(() => {
    window.addEventListener("keydown", keydownHandler);
    window.addEventListener("mousedown", mousedownHandler);

    return () => {
      window.removeEventListener("keydown", keydownHandler);
      window.removeEventListener("mousedown", mousedownHandler);
    };
  }, []);

  if (!isVisible) {
    return <></>;
  }

  return (
    <div className={styles.search_modal_wrapper}>
      <div className={styles.search_bar_wrapper} ref={searchBarRef}>
        <SearchBar />
      </div>
    </div>
  );
};

export default SearchModal;
