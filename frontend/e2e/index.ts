import { test } from "@playwright/test";

import { crawlTests } from "./tests/crawl";
import { createBrainTests } from "./tests/createBrain";

test.describe(createBrainTests);

test.describe(crawlTests);
