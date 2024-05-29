/* eslint-disable max-lines */
module.exports = {
  plugins: ["prefer-arrow", "import"],
  extends: [
    "next",
    "next/core-web-vitals",
    "eslint:recommended",
    "plugin:import/recommended",
  ],
  ignorePatterns: ["**/node_modules/", "**/.next/"],
  rules: {
    "import/extensions": 0,
    "import/no-unresolved": 0,
    "import/prefer-default-export": 0,
    "import/no-duplicates": "error",
    complexity: ["error", 10],
    "max-lines": ["error", 300],
    "max-depth": ["error", 3],
    "max-params": ["error", 5],
    eqeqeq: ["error", "smart"],
    "import/no-extraneous-dependencies": [
      "error",
      {
        devDependencies: true,
        optionalDependencies: false,
        peerDependencies: false,
      },
    ],
    "no-shadow": [
      "error",
      {
        hoist: "all",
      },
    ],
    "prefer-const": "error",
    "import/order": [
      "error",
      {
        pathGroups: [{ pattern: "@lib/**", group: "unknown" }],
        groups: [
          ["external", "builtin"],
          "unknown",
          "internal",
          "sibling",
          "parent",
          "index",
        ],
        alphabetize: {
          order: "asc",
          caseInsensitive: false,
        },
        "newlines-between": "always",
        pathGroupsExcludedImportTypes: ["builtin"],
      },
    ],
    "import/namespace": "off",
    "sort-imports": [
      "error",
      {
        ignoreCase: true,
        ignoreDeclarationSort: true,
        ignoreMemberSort: false,
        memberSyntaxSortOrder: ["none", "all", "multiple", "single"],
      },
    ],
    "padding-line-between-statements": [
      "error",
      {
        blankLine: "always",
        prev: "*",
        next: "return",
      },
    ],
    "prefer-arrow/prefer-arrow-functions": [
      "error",
      {
        disallowPrototype: true,
        singleReturnOnly: false,
        classPropertiesAllowed: false,
      },
    ],
    "no-restricted-imports": [
      "error",
      {
        paths: [
          {
            name: "lodash",
            message: "Please use lodash/{module} import instead",
          },
          {
            name: "aws-sdk",
            message: "Please use aws-sdk/{module} import instead",
          },
          {
            name: ".",
            message: "Please use explicit import file",
          },
        ],
      },
    ],
    curly: ["error", "all"],
  },
  root: true,
  env: {
    es6: true,
    node: true,
    browser: true,
  },
  parserOptions: {
    ecmaVersion: 2021,
    sourceType: "module",
    babelOptions: {
      presets: [require.resolve("next/babel")],
    },
  },
  overrides: [
    {
      files: ["**/*.ts?(x)"],
      extends: [
        "plugin:@typescript-eslint/recommended",
        "plugin:@typescript-eslint/recommended-requiring-type-checking",
        "plugin:import/typescript",
      ],
      parser: "@typescript-eslint/parser",
      parserOptions: {
        project: "./tsconfig.eslint.json",
        tsconfigRootDir: __dirname,
        sourceType: "module",
      },
      rules: {
        "@typescript-eslint/prefer-optional-chain": "error",
        "react-hooks/exhaustive-deps": "off",
        "no-shadow": "off",
        "@typescript-eslint/no-shadow": "error",
        "@typescript-eslint/prefer-nullish-coalescing": "error",
        "@typescript-eslint/ban-ts-comment": [
          "error",
          {
            "ts-ignore": "allow-with-description",
            minimumDescriptionLength: 10,
          },
        ],
        "@typescript-eslint/explicit-function-return-type": 0,
        "@typescript-eslint/explicit-member-accessibility": 0,
        "@typescript-eslint/camelcase": 0,
        "@typescript-eslint/interface-name-prefix": 0,
        "@typescript-eslint/explicit-module-boundary-types": "error",
        "@typescript-eslint/no-explicit-any": "error",
        "@typescript-eslint/no-unused-vars": "error",
        "@typescript-eslint/ban-types": [
          "error",
          {
            types: {
              FC: "Use `const MyComponent = (props: Props): JSX.Element` instead",
              SFC: "Use `const MyComponent = (props: Props): JSX.Element` instead",
              FunctionComponent:
                "Use `const MyComponent = (props: Props): JSX.Element` instead",
              "React.FC":
                "Use `const MyComponent = (props: Props): JSX.Element` instead",
              "React.SFC":
                "Use `const MyComponent = (props: Props): JSX.Element` instead",
              "React.FunctionComponent":
                "Use `const MyComponent = (props: Props): JSX.Element` instead",
            },
            extendDefaults: true,
          },
        ],
        "@typescript-eslint/no-unnecessary-boolean-literal-compare": "error",
        "@typescript-eslint/no-unnecessary-condition": "error",
        "@typescript-eslint/no-unnecessary-type-arguments": "error",
        "@typescript-eslint/prefer-string-starts-ends-with": "error",
        "@typescript-eslint/switch-exhaustiveness-check": "error",
        "@typescript-eslint/restrict-template-expressions": "off",
      },
    },
  ],
};
