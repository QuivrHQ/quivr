import { AiFillLinkedin } from "react-icons/ai";
import { RiTwitterXFill } from "react-icons/ri";

import { Testimonial } from "../types";

export const socialMediaToIcon: Record<
  Testimonial["socialMedia"],
  JSX.Element
> = {
  linkedin: <AiFillLinkedin />,
  x: <RiTwitterXFill />,
};
