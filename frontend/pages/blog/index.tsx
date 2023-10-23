/* eslint-disable */
/* https://strapi.io/blog/how-to-create-an-ssg-static-site-generation-application-with-strapi-webhooks-and-nextjs */
import type { InferGetStaticPropsType } from 'next';
import Head from "next/head";
import Image from "next/image";
import Link from "next/link";

import "@/globals.css";

type BlogPostAttributes = {
  imageUrl: string;
  title: string;
  description: string;
  slug: string;
  publishedAt: string;
  seo: {
    metaTitle: string;
    metaDescription: string;
    metaImage: {
      data: {
        attributes: {
          formats: {
            medium: {
              url: string;
            };
          };
        };
      };
    };
  };
};

type BlogPost = {
  id: string;
  attributes: BlogPostAttributes;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const getStaticProps = async () => {
  try {
    const resulting = await fetch("https://cms.quivr.app/api/blogs?populate=seo,seo.metaImage,slug");
    const data: { data: BlogPost[] } = await resulting.json();

    // Sort blogs by publishedAt in descending order
    const sortedBlogs = data.data.sort((a, b) => new Date(b.attributes.publishedAt).getTime() - new Date(a.attributes.publishedAt).getTime());

    return {
      props: {
        result: sortedBlogs,
      },
    };
  } catch (error) {
    console.error("Error fetching blogs:", error);

    return {
      notFound: true, // this will return a 404 page
    };
  }
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
const Blog = ({ result }: InferGetStaticPropsType<typeof getStaticProps>) => {
  return (
    <div>
      <section className="w-full">
        <Head>
          <title>Quivr - Blog</title>
          <meta name="description" content="Quivr.app - Your Generative AI second brain builder's blog" />
        </Head>

        <header className="bg-white text-zinc-900 py-4 border-b">
          <div className="container mx-auto px-4 md:px-6">
            <nav className="flex items-center justify-between">
              <Link href="/blog">
                <div className="text-2xl font-bold cursor-pointer">Quivr</div>
              </Link>
              <div className="space-x-4">
                <Link className="text-zinc-900 hover:text-zinc-700" href="/">Try Quivr</Link>
              </div>
            </nav>
          </div>
        </header>

        <main className="container mx-auto px-4 md:px-6 py-8">
          <section className="mb-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {result.map(post => (
                <div key={post.id}>
                  <Link href={`/blog/${post.attributes.slug}`}>
                    <Image
                      src={`${post.attributes.seo.metaImage.data.attributes.formats.medium.url}`}
                      alt="Blog Post Image"
                      width={600}
                      height={400}
                      className="w-full rounded-lg object-cover cursor-pointer"
                    />
                  </Link>
                  <h3 className="text-xl font-bold mb-2 mt-4">{post.attributes.seo.metaTitle}</h3>
                  <p className="text-zinc-500">{post.attributes.seo.metaDescription}</p>
                  <Link className="text-blue-500 hover:text-blue-700 mt-4" href={`/blog/${post.attributes.slug}`}>
                    Read More
                  </Link>
                </div>
              ))}
            </div>
          </section>
        </main>
      </section>
    </div>
  );
}

export default Blog;