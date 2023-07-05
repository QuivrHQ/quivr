import { renderHook } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { getNock } from "../../tests/getNock";
import { useChatApi } from "../useChatApi";

getNock().options("/chat").reply(200);

describe("useChatApi", () => {
  it("should make http request while creating chat", async () => {
    const chatName = "Test Chat";

    const scope = getNock().post("/chat").reply(200, { chat_name: chatName });

    const {
      result: {
        current: { createChat },
      },
    } = renderHook(() => useChatApi());

    const createdChat = await createChat(chatName);

    //Check that the endpoint was called
    expect(scope.isDone()).toBe(true);

    expect(createdChat).toMatchObject({ chat_name: chatName });
  });
});
