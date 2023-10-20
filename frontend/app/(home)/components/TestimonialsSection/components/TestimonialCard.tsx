import Link from "next/link";

import { Avatar } from "@/lib/components/ui/Avatar";
import { Testimonial } from "@/lib/types/testimonial";

import { socialMediaToIcon } from "../utils/socialMediaToIcon";

export const TestimonialCard = ({
  socialMedia,
  url,
  name,
  jobTitle,
  content,
  profilePicture,
}: Testimonial): JSX.Element => {
  return (
    <div className="px-8 py-4 rounded-3xl shadow-2xl dark:shadow-white/25  w-full bg-white dark:bg-black h-full flex flex-col gap-3">
      <Link
        href={url}
        className="hover:text-black"
        target="_blank"
        rel="noopener noreferrer"
      >
        <div className="w-full flex justify-end">
          {socialMediaToIcon[socialMedia]}
        </div>
      </Link>

      <p className="flex-1 italic">&quot;{content}&quot;</p>
      <div>
        <div className="flex mt-3 flex-1 items-center">
          <Avatar
            url={profilePicture ?? "https://www.gravatar.com/avatar?d=mp"}
            alt={`${name}-profile`}
            imgClassName={"rounded-full"}
            className="w-10 h-10"
          />
          <div className="flex-1 ml-3">
            <p className="font-semibold">{name}</p>
            <p className="text-sm">{jobTitle}</p>
          </div>
        </div>
      </div>
    </div>
  );
};
