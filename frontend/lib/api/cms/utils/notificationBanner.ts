import { AxiosInstance } from "axios";

import { NotificationBanner } from "@/lib/types/NotificationBanner";

type CmsNotificationBanner = {
  data: {
    attributes: {
      text: string;
      notification_id: string;
      style?: Record<string, string>;
      dismissible?: boolean;
      isSticky?: boolean;
    };
  };
};

const mapCmsNotificationBannerToNotificationBanner = (
  cmsNotificationBanner: CmsNotificationBanner
): NotificationBanner => ({
  text: cmsNotificationBanner.data.attributes.text,
  id: cmsNotificationBanner.data.attributes.notification_id,
  style: cmsNotificationBanner.data.attributes.style,
  dismissible: cmsNotificationBanner.data.attributes.dismissible,
  isSticky: cmsNotificationBanner.data.attributes.isSticky,
});

export const getNotificationBanner = async (
  axiosInstance: AxiosInstance
): Promise<NotificationBanner> => {
  const response = await axiosInstance.get<CmsNotificationBanner>(
    "/api/notification-banner"
  );

  return mapCmsNotificationBannerToNotificationBanner(response.data);
};
