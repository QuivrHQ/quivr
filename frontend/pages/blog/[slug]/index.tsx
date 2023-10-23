/* eslint-disable */
'use client';
import type { GetStaticPaths, InferGetStaticPropsType } from 'next';
import Head from 'next/head';
import Image from "next/image";
import Link from 'next/link';
import { useEffect, useState } from 'react';

import "@/globals.css";


type SeoAttributes = {
  id: number;
  metaTitle: string;
  metaDescription: string;
  metaImage: {
    id: number;
    data: {
      attributes: {
        formats: {
          large: {
            url: string;
          };
          medium: {
            url: string;
          };
        };
      };
    };
  };
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
  slug: string;
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
      throw new Error('Network response was not ok');
    }
    const data: { data: BlogPost[] } = await response.json();
    const paths = data.data.map(post => ({ params: { slug: post.attributes.slug } }));

    return {
      paths,
      fallback: false,
    };
  } catch (error) {
    console.error("Error fetching blog paths:", error);
    return {
      paths: [],
      fallback: false,
    };
  }
};

export const getStaticProps = async (context: { params: { slug: string } }) => {
  try {
    const response = await fetch(`https://cms.quivr.app/api/blogs?slug=${context.params.slug}&populate=seo,seo.metaImage`);
    const data: { data: BlogPost[] } = await response.json();

    // Find the blog post with the exact slug match
    const blogPost = data.data.find(post => post.attributes.slug === context.params.slug);

    if (!blogPost) {
      throw new Error('No blog post found for the provided slug');
    }

    return {
      props: {
        post: blogPost,
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
  const { metaTitle, metaDescription, keywords, canonicalURL } = post.attributes.seo;

  // Extract different image formats
  const { large, medium } = post.attributes.seo.metaImage.data.attributes.formats;

  const [imageUrl, setImageUrl] = useState(medium.url);

  useEffect(() => {
    // Determine which image URL to use once the component has mounted on the client side
    setImageUrl(window.innerWidth > 768 ? large.url : medium.url);
  }, []);

  return (
    <section className="w-full">
      <header className="bg-white text-zinc-900 py-4 border-b">
        <div className="container mx-auto px-4 md:px-6">
          <nav className="flex items-center justify-between">
            <Link href="/blog">
              <div className="text-2xl font-bold cursor-pointer">Quivr</div>
            </Link>
            <div className="space-x-4">
              <Link className="text-zinc-900 hover:text-zinc-700" href="https://quivr.app">Try Quivr</Link>
            </div>
          </nav>
        </div>
      </header>
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
          <Image
            src={imageUrl}
            alt={metaTitle}
            className="aspect-video overflow-hidden rounded-lg object-cover"
            width={1250}
            height={340}
          />
          <div className="text-black dark:text-white" dangerouslySetInnerHTML={{ __html: post.attributes.Article }}></div>
        </article>
      </div>
    </section>
  );
}

export default BlogPostDetail;