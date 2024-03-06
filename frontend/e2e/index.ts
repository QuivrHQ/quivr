import { test } from "@playwright/test";

import { crawlTests } from "./tests/crawl";
import { createBrainTests } from "./tests/createBrain";
import { threadTests } from "./tests/thread";

test.describe(createBrainTests);

test.describe(crawlTests);

test.describe(threadTests);
