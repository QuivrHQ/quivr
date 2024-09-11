declare module "file-icons-js" {
  interface FileIcons {
    getClassWithColor: (extension: string) => string;
  }

  const fileIcons: FileIcons;
  export default fileIcons;
}
