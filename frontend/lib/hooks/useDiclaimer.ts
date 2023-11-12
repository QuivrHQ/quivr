"use client";

import { useEffect, useState } from "react";

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const useDiclaimer = () => {
  const [visibleDisclaimer, setVisibleDisclaimer] = useState<boolean>(true);

  const WEEK_TIME = 7 * 24 * 3600 * 1000;

  const close_disclaimer_time = localStorage.getItem("close_disclaimer_time");

  const handleCloseDisclaimer = () => {
    setVisibleDisclaimer(false);

    const closeTime = new Date().getTime();
    localStorage.setItem("close_disclaimer_time", closeTime.toString());
  };

  useEffect(() => {
    checkDiclaimerVisible();
  }, []);

  const checkDiclaimerVisible = () => {
    if (close_disclaimer_time === null) {
      return;
    }
    updateDisclaimerNextVisibleTime();
  };

  const updateDisclaimerNextVisibleTime = () => {
    const diff = new Date().getTime() - Number(close_disclaimer_time);
    if (diff >= WEEK_TIME) {
      setVisibleDisclaimer(true);
    } else {
      setVisibleDisclaimer(false);
    }
  };

  return {
    visibleDisclaimer,
    handleCloseDisclaimer,
  };
};
