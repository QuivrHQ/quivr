/* eslint-disable */
'use client';
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
};

type BlogPost = {
  id: string;
  attributes: BlogPostAttributes;
};

// eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
export const getStaticProps = async () => {
  try {
    const resulting = await fetch("https://cms.quivr.app/api/blogs");
    // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
    const data: { data: BlogPost[] } = await resulting.json();

    return {
      props: {
        result: data.data,
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
    <main className="bg-white min-h-screen p-8 text-gray-900">
      <Head>
        <title>Quivr - Blog</title>
        <meta name="description" content="Quivr.app - Your Generative AI second brain builder's blog" />
      </Head>
      <div className="mx-auto container">
        <h1 className="text-6xl font-extrabold mb-16 text-center tracking-tight text-black">Blog Posts</h1>
        <div className="grid gap-16 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
          {result.map((post, index) => {
            if (index === 0) {
              // Special layout for the first post
              return (
                <Link
                  href={`/blog/${post.id}`}
                  key={post.id}
                  className="col-span-full block p-8 bg-white border-2 border-gray-300 rounded-lg shadow-md hover:border-black hover:shadow-xl transform hover:scale-105 transition-transform duration-200 flex"
                >
                  <div className="flex-1 pr-8">
                    <h2 className="text-4xl font-bold mb-4 group-hover:text-black transition-colors duration-200">{post.attributes.title}</h2>
                    <p className="text-gray-600 line-clamp-3">{post.attributes.description}</p>
                  </div>
                  <div className="flex-none">
                    <Image
                      src={`${post.attributes.imageUrl}`}
                      alt="blog-post"
                      width={400}
                      height={400}
                      className="rounded-lg object-cover"
                    />
                  </div>
                </Link>
              );
            } else {
              // Standard layout for the rest of the posts
              return (
                <Link
                  href={`/blog/${post.id}`}
                  key={post.id}
                  className="block p-8 bg-white border-2 border-gray-300 rounded-lg shadow-md hover:border-black hover:shadow-xl transform hover:scale-105 transition-transform duration-200"
                >
                  <div className="mb-6">
                    <Image
                      src={`${post.attributes.imageUrl}`}
                      alt="blog-post"
                      width={300}
                      height={300}
                      className="w-full rounded-lg object-cover"
                    />
                  </div>
                  <h2 className="text-3xl font-bold mb-4 group-hover:text-black transition-colors duration-200">{post.attributes.title}</h2>
                  <p className="text-gray-600 line-clamp-3">{post.attributes.description}</p>
                </Link>
              );
            }
          })}
        </div>
      </div>
    </main>
  );
}




export default Blog;
