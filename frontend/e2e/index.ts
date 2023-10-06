import { test } from "@playwright/test";

import { chatTests } from "./tests/chat";
import { crawlTests } from "./tests/crawl";
import { createBrainTests } from "./tests/createBrain";

test.describe(createBrainTests);

test.describe(crawlTests);

test.describe(chatTests);
