import Script from "next/script";

export const GoogleAnalytics = (): JSX.Element => {
  const ga_id = process.env.NEXT_PUBLIC_GA_ID;

  if (ga_id === undefined) {
    return <></>;
  }

  return (
    <>
      <Script
        async
        src={`https://www.googletagmanager.com/gtag/js?id=${ga_id}`}
      />
      <Script
        id="ga-config"
        dangerouslySetInnerHTML={{
          __html: `
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${ga_id}');
        `,
        }}
      />
    </>
  );
};
