'use client';
/* https://strapi.io/blog/how-to-create-an-ssg-static-site-generation-application-with-strapi-webhooks-and-nextjs */
import type { InferGetStaticPropsType } from 'next';
import Head from "next/head";
import Image from "next/image";
import Link from "next/link";


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
    <main className="bg-gray-100 min-h-screen p-8">
      <Head>
        <title>thisBlog</title>
        <meta name="description" content="This is an example of our blog" />
      </Head>
      <div className="max-w-screen-xl mx-auto">
        <h1 className="text-4xl font-bold mb-12 text-center">Blog Posts</h1>
        <div className="grid gap-12 grid-cols-1 md:grid-cols-2">
          {result.map(post => (
            <Link href={`/blog/${post.id}`} key={post.id}>
              <div className="block p-8 bg-white rounded-lg shadow-md hover:shadow-xl transform hover:scale-105 transition-transform duration-200">
                <div className="mb-6">
                  <Image
                    src={`${post.attributes.imageUrl}`}
                    alt="blog-post"
                    priority={true}
                    className="w-full rounded-lg object-cover h-56"
                    width={600}
                    height={300}
                  />
                </div>
                <h2 className="text-2xl font-semibold mb-4">{post.attributes.title}</h2>
                <p className="text-gray-600">{post.attributes.description}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}

export default Blog;
