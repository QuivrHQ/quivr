import { test } from "@playwright/test";

import { chatTests } from "./tests/chat";
import { createBrainTests } from "./tests/createBrain";
import { uploadTests } from "./tests/upload";

test.describe(createBrainTests);

test.describe.skip(uploadTests);

test.describe.skip(chatTests);
