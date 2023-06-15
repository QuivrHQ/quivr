module.exports = {
  "*": "prettier --ignore-unknown --write",
  "*.{js,ts, tsx}": "pnpm lint-fix",
};
