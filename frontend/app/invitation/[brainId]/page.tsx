"use client";

import Button from "@/lib/components/ui/Button";
import PageHeading from "@/lib/components/ui/PageHeading";
import Spinner from "@/lib/components/ui/Spinner";
import { useSupabase } from "@/lib/context/SupabaseProvider";
import { redirectToLogin } from "@/lib/router/redirectToLogin";

import { useInvitation } from "./hooks/useInvitation";

const InvitationPage = (): JSX.Element => {
  const { handleAccept, handleDecline, isLoading } = useInvitation();
  const { session } = useSupabase();
  // Show the loader while invitation validity is being checked
  if (isLoading) {
    return <Spinner />;
  }

  // TODO: Modify this to fetch the brain name from the database
  const brain = { name: "TestBrain" };

  if (session?.user === undefined) {
    redirectToLogin();
  }

  return (
    <main className="pt-10">
      <PageHeading
        title={`Welcome to ${brain.name}!`}
        subtitle="You have been exclusively invited to join this brain and start exploring. Do you accept this exciting journey?"
      />
      <div className="flex flex-col items-center justify-center gap-5 mt-5">
        <Button
          onClick={() => void handleAccept()}
          variant={"secondary"}
          className="py-3"
        >
          Yes, count me in!
        </Button>
        <Button
          onClick={() => void handleDecline()}
          variant={"danger"}
          className="py-3"
        >
          No, thank you.
        </Button>
      </div>
    </main>
  );
};

export default InvitationPage;
