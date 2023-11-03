"use client";
// eslint-disable-next-line import/no-extraneous-dependencies
import {
  EmailIcon,
  EmailShareButton,
  RedditIcon,
  RedditShareButton,
  TelegramIcon,
  TelegramShareButton,
  TwitterIcon,
  TwitterShareButton,
  WeiboIcon,
  WeiboShareButton,
  WhatsappIcon,
  WhatsappShareButton,
} from "next-share";

export const SharePlatform = ({
  chatShareURL,
}: {
  chatShareURL: string;
}): JSX.Element => {
  const title = `vaccinetruth.ai`;

  return (
    <div className="flex-center flex-wrap flex">
      <div className="mr-4">
        <WhatsappShareButton url={chatShareURL} title={title} separator=":: ">
          <WhatsappIcon size={32} round />
        </WhatsappShareButton>
      </div>
      <div className="mr-4">
        <TwitterShareButton url={chatShareURL} title={title}>
          <TwitterIcon size={32} round />
        </TwitterShareButton>
      </div>
      <div className="mr-4">
        <EmailShareButton url={chatShareURL} subject={title} body="body">
          <EmailIcon size={32} round />
        </EmailShareButton>
      </div>
      <div className="mr-4">
        <RedditShareButton url={chatShareURL} title={title}>
          <RedditIcon size={32} round />
        </RedditShareButton>
      </div>
      <div className="mr-4">
        <TelegramShareButton url={chatShareURL} title={title}>
          <TelegramIcon size={32} round />
        </TelegramShareButton>
      </div>
      <div className="mr-4">
        <WeiboShareButton url={chatShareURL} title={title}>
          <WeiboIcon size={32} round />
        </WeiboShareButton>
      </div>
    </div>
  );
};
