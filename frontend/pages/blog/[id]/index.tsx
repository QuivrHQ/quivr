/* eslint-disable */
import type { GetStaticPaths, InferGetStaticPropsType } from 'next';
import Head from "next/head";
import Image from "next/image";


type SeoAttributes = {
  id: number;
  metaTitle: string;
  metaDescription: string;
  metaImage: string;
  keywords: string;
  metaRobots: string | null;
  structuredData: string | null;
  metaViewport: string | null;
  canonicalURL: string | null;
};

type BlogPostAttributes = {
  title: string; // Assuming title is extracted from the first few words of the article
  Article: string;
  createdAt: string;
  updatedAt: string;
  publishedAt: string;
  seo: SeoAttributes;
};

type BlogPost = {
  id: number;
  attributes: BlogPostAttributes;
};


export const getStaticPaths: GetStaticPaths = async () => {
  try {
    const response = await fetch("https://cms.quivr.app/api/blogs");
    if (!response.ok) {
      throw new Error('Network response was not ok');  // Handle non-200 responses
    }
    const data: { data: BlogPost[] } = await response.json();
    const paths = data.data.map(post => ({ params: { id: post.id.toString() } }));
    
    return {
      paths,
      fallback: false,  // Use "true" to enable ISR (Incremental Static Regeneration) or "blocking" for server-side rendering fallback
    };
  } catch (error) {
    console.error("Error fetching blog paths:", error);
    return {
      paths: [],  // Return empty array if there's an error
      fallback: false,  // Use "true" to enable ISR or "blocking" for server-side rendering fallback
    };
  }
};




export const getStaticProps = async (context: { params: { id: string } }) => {
  try {
    const response = await fetch(`https://cms.quivr.app/api/blogs/${context.params.id}?populate=seo`);
    console.log(response)
    const data: { data: BlogPost } = await response.json();
    

    return {
      props: {
        post: data.data,
      },
    };
  } catch (error) {
    console.error("Error fetching blog post:", error);

    return {
      notFound: true,
    };
  }
};

const BlogPostDetail = ({ post }: InferGetStaticPropsType<typeof getStaticProps>) => {
  const { metaTitle, metaDescription, keywords, canonicalURL, metaImage } = post.attributes.seo;

  return (
    <div className="px-4 py-6 md:px-6 lg:py-16 md:py-12 bg-white dark:bg-black">
      <Head>
        <title>{metaTitle}</title>
        <meta name="description" content={metaDescription} />
        <meta name="keywords" content={keywords} />
        {canonicalURL && <link rel="canonical" href={canonicalURL} />}
      </Head>
      <article className="prose prose-zinc mx-auto dark:prose-invert">
        <div className="space-y-2 not-prose">
          <h1 className="text-4xl font-extrabold tracking-tight lg:text-5xl lg:leading-[3.5rem] text-black dark:text-white">
            {metaTitle}
          </h1>
          <p className="text-zinc-500 dark:text-zinc-400">Posted on {post.attributes.publishedAt}</p>
        </div>
        <p className="text-black dark:text-white">
          {metaDescription}
        </p>
        <figure>
          {/* Assuming you'd extract the image URL from the Article content */}
          <Image
            src={metaImage}
            alt={metaTitle}
            className="aspect-video overflow-hidden rounded-lg object-cover"
            width={1250}
            height={340}
          />
          <figcaption className="text-black dark:text-white">{metaTitle}</figcaption>
        </figure>
        {/* Insert the HTML content directly */}
        <div dangerouslySetInnerHTML={{ __html: post.attributes.Article }}></div>
      </article>
    </div>
  );
}

export default BlogPostDetail;