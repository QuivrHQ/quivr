import { AiFillLinkedin } from "react-icons/ai";
import { RiTwitterXFill } from "react-icons/ri";

import { Testimonial } from "@/lib/types/Testimonial";

export const socialMediaToIcon: Record<
  Testimonial["socialMedia"],
  JSX.Element
> = {
  linkedin: <AiFillLinkedin />,
  x: <RiTwitterXFill />,
};
