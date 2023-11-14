import type { Metadata, ResolvingMetadata } from 'next';

import { DisplayChatMessageArea } from '@/lib/components/DisplayChatMessageArea';

import TalkToVT from '../../components/TalkToVT';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Props = { params: { lng: string } };
export const generateMetadata = async (
  { params: { lng = 'en' } }: Props,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  parent?: ResolvingMetadata
): Promise<Metadata> => {
  return {
    title: `vaccinetruth.ai`,
    description: `vaccinetruth.ai`,
    openGraph: {
      images: [
        {
          url: 'https://vaccinetruth.ai/vt-logo-256.png',
          width: 256,
          height: 256,
        },
      ],
      locale: lng,
    },
  };
};

const SharedChatPage = (): JSX.Element => {
  return (
    <div
      className={`flex flex-col flex-1 items-center justify-stretch w-full h-fill-available overflow-hidden  dark:bg-black transition-colors ease-out duration-500`}
      data-testid="chat-page"
    >
      <div className="py-4 text-center border-b border-solid w-full text-xs sm:text-sm">
        Shared Chat • Vaccine truth knowledge base v1.0.1
      </div>
      <div
        className={`flex flex-col flex-1 w-full h-full dark:shadow-primary/25 overflow-hidden `}
      >
        <div className="flex flex-1 flex-col overflow-y-auto ">
          <DisplayChatMessageArea />
        </div>
      </div>
      <TalkToVT />
    </div>
  );
};

export default SharedChatPage;
