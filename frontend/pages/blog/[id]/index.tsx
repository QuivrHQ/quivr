/* eslint-disable */
import type { GetStaticPaths, InferGetStaticPropsType } from 'next';
import Head from "next/head";
import Image from "next/image";

type BlogPostAttributes = {
  imageUrl: string;
  title: string;
  description: string;
  draft: string;
};

type BlogPost = {
  id: string;
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
    const response = await fetch(`https://cms.quivr.app/api/blogs/${context.params.id}`);
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
  return (
    <main className="bg-gray-100 min-h-screen p-8">
      <Head>
        <title>{post.attributes.title}</title>
        <meta name="description" content={post.attributes.description} />
      </Head>
      <div className="max-w-screen-xl mx-auto">
        <div className="bg-white p-8 rounded-lg shadow-md">
          <Image
            src={post.attributes.imageUrl}
            alt="blog-post-detail"
            className="w-full rounded-t-lg object-cover h-56"
            width={1000}
            height={500}
          />
          <h1 className="text-4xl font-bold my-6">{post.attributes.title}</h1>
          <p className="text-gray-700 whitespace-pre-line">{post.attributes.draft}</p>
        </div>
      </div>
    </main>
  );
}

export default BlogPostDetail;
