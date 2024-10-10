# 🗄️ Storage

## Your Brain’s File Management System

The `Storage` class is the backbone of how a brain interacts with files in `quivr-core`. Every brain holds a reference to an underlying storage system to manage its files. All storages should implement the `StorageBase` base classe that provides the structure and methods to make that happen seamlessly. Let's walk through how it works:

- **Brain-Storage Connection:** Your brain holds a reference to a storage system. This class is the main way your brain can interact with and manage the files it uses. Adding files to a brain will upload them to the storage. This means that files in the storage are stored **before** processing!
- **File Management:** the storage holds a set of `QuivrFile` objects, which are the building blocks of your brain’s file system. The storage can store them remotely or locally or hold simple

### What can you do with this storage system?

1. Upload Files: You can add new files to your storage whenever you need. The system also lets you decide whether to overwrite existing files or not.
2. Get Files: Need to see what's in your storage? No problem. You can easily retrieve a list of all the files that are stored.
3. Delete Files: Clean-up is simple. You can remove any file from your storage by referencing its unique file ID (more on that in `QuivrFile`).

StorageBase is the foundation of how your brain organizes, uploads, retrieves, and deletes its files. It ensures that your brain can always stay up-to-date with the files it needs, making file management smooth and intuitive. You can build your own storage system by subclassing the `StorageBase` class and passing it to the brain. See [custom_storage](../examples/custom_storage.md) for more details.

### Storage Implementations in `quivr_core`

`quivr_core` currently offers two storage implementations: `LocalStorage` and `TransparentStorage`:

- **LocalStorage**:  
  This storage type is perfect when you want to keep files on your local machine. `LocalStorage` saves your files to a specific directory, either a default path (`~/.cache/quivr/files`) or a user-defined location. It can store files by copying them or by creating symbolic links to the original files, based on your preference. This storage type also keeps track of file hashes to prevent accidental overwrites during uploads.

- **TransparentStorage**:  
  The `TransparentStorage` implementation offers a lightweight and flexible approach, mainly managing files in memory without a need for local file paths. This storage system is useful when you don't need persistent storage but rather an easy way to store and retrieve files temporarily during the brain's operation.

Each of these storage systems has its own strengths, catering to different use cases. As `quivr_core` evolves, we will implementat more ande more storage systems allowing for even more advanced and customized ways to manage your files like `S3Storage`, `NFSStorage` ...
