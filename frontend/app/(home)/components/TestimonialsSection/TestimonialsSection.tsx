import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

import { TESTIMONIALS_DATA_KEY } from "@/lib/api/cms/config";
import { useCmsApi } from "@/lib/api/cms/useCmsApi";
import Spinner from "@/lib/components/ui/Spinner";

import { TestimonialCard } from "./components/TestimonialCard";

export const TestimonialsSection = (): JSX.Element => {
  const { t } = useTranslation("home", {
    keyPrefix: "testimonials",
  });

  const { getTestimonials } = useCmsApi();

  const { data: testimonials, isLoading } = useQuery({
    queryKey: [TESTIMONIALS_DATA_KEY],
    queryFn: getTestimonials,
  });

  if (isLoading || !testimonials) {
    return <Spinner />;
  }

  return (
    <>
      <p className="text-4xl font-semibold my-10">
        {t("title")} <span className="text-primary">Quivr</span>{" "}
      </p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-10 mb-5 items-stretch p-4">
        {testimonials.map((testimonial) => (
          <div key={testimonial.content}>
            <TestimonialCard {...testimonial} />
          </div>
        ))}
      </div>
    </>
  );
};
