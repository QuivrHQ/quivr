import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { TestimonialCard } from "./components/TestimonialCard";
import { testimonialsExamples } from "./data/testimonialsExamples";
import { Testimonial } from "./types";

export const TestimonialsSection = (): JSX.Element => {
  const { t } = useTranslation("home", {
    keyPrefix: "testimonials",
  });

  const [testimonials, setTestimonials] = useState<Testimonial[]>([]);

  useEffect(() => {
    setTestimonials(testimonialsExamples);
  }, []);

  return (
    <>
      <p className="text-4xl font-semibold my-10">
        {t("title")} <span className="text-primary">Quivr</span>{" "}
      </p>
      <div className="grid grid-cols-12 gap-10 mb-5 items-stretch p-4">
        {testimonials.map((testimonial) => (
          <div
            className="col-span-12 md:col-span-4 h-full"
            key={testimonial.content}
          >
            <TestimonialCard {...testimonial} />
          </div>
        ))}
      </div>
    </>
  );
};
