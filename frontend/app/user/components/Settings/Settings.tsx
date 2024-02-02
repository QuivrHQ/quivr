import { useState } from "react";

import { TextInput } from "@/lib/components/ui/TextInput/TextInput";

export const Settings = (): JSX.Element => {
  const [username, setUsername] = useState<string>("");

  return (
    <div>
      <TextInput
        label="Username"
        iconName="user"
        inputValue={username}
        setInputValue={setUsername}
      />
    </div>
  );
};
