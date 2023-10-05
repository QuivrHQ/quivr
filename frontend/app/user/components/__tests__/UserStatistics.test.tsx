import { describe, expect, it } from "vitest";

import { formatBrainSizeUsage } from "../UserStatistics";

describe("UserStatistics", () => {
  describe("formatBrainSize", () => {
    it("should return string", () => {
      const result = formatBrainSizeUsage(1, 5);

      expect(typeof result).toBe("string");
    });

    it.each([
      { input: { currentBrainSize: 1, maxBrainSize: 2 }, expected: true },
      { input: { currentBrainSize: 0, maxBrainSize: 0 }, expected: true },
      { input: { currentBrainSize: 1000, maxBrainSize: 5000 }, expected: true },
      {
        input: { currentBrainSize: 1337, maxBrainSize: 2674 },
        expected: true,
      },
      { input: { currentBrainSize: 5000, maxBrainSize: 1000 }, expected: true },
    ])(
      "formatBrainSizeUsage($input.currentBrainSize, $input.maxBrainSize) -> $expected",
      ({ input, expected }) => {
        const formatRegex = /^(.+?)\s+\/\s+(.+?)$/gm;
        const result = formatBrainSizeUsage(
          input.currentBrainSize,
          input.maxBrainSize
        );
        const match = formatRegex.test(result);

        expect(typeof result).toBe("string");
        expect(match).toBe(expected);
      }
    );
  });
});
