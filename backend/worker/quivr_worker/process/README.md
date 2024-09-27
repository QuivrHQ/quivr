# Knowledge Processing

## Steps for Processing

1. The task receives a `knowledge_id: UUID`.
2. The `KnowledgeProcessor.process_knowledge` method processes the knowledge:
   - It constructs a processable tuple of `[Knowledge, QuivrFile]` stream:
     - Retrieves the `KnowledgeDB` object from the database.
     - Determines the processing steps based on the knowledge source:
       - **Local**:
         - Downloads the knowledge data from S3 storage and writes it to a temporary file.
         - Yields the `[Knowledge, QuivrFile]`.
       - **Web**: Processes similarly to the **Local** method.
       - **[Syncs]**:
         - Fetches the associated sync and verifies the credentials.
         - Concurrently retrieves all knowledges for the user from the database associated with this sync, as well as the tree of sync files where this knowledge is the parent (using the sync provider).
         - Downloads the knowledge and yields the initial `[Knowledge, QuivrFile]` that the task received.
         - For all children of this knowledge (i.e., those fetched from the sync):
           - If the child exists in the database (i.e., knowledge where `knowledge.sync_id == sync_file.id`):
             - This implies that the sync's child knowledge might have been processed earlier in another brain.
             - If the knowledge has been PROCESSED, link it to the parent brains and continue.
             - If not, reprocess the file.
           - If the child does not exist:
             - Create the knowledge associated with the sync file and set it to `Processing`.
             - Download the sync file's data and yield the `[Knowledge, QuivrFile]`.
   - Skip processing of the tuple if the knowledge is a folder.
   - Parse the `QuivrFile` using `quivr-core`.
   - Store the resulting chunks in the database.
   - Update the knowledge status to `PROCESSED`.

### Handling Exceptions During Parsing Loop

#### Catchable Errors:

If an exception occurs during the parsing loop, the following steps are taken:

1. Roll back the current transaction (this only affects the vectors) if they were set. The processing loop performs the following stateful operations in this order:
   - Creating knowledges (with `Processing` status).
   - Downloading sync files from sync provider
   - Updating knowledges: linking them to brains.
   - Creating vectors.
   - Updating knowledges.

**Transaction Safety for Each Operation:**

- **Creating knowledge and linking to brains**: These operations can be retried safely. Knowledge is only recreated if it does not already exist in the database, allowing for safe retry.
- **Downloading sync files**: This operation is idempotent but is safe to retry. If a change has occured, we would download the last version of the file.
- **Linking knowledge to brains**: Only links the brain if it is not already associated with the knowledge. Safe for retry.
- **Creating vectors**:
  - This operation should be rolled back if an error occurs afterward. Otherwise, the knowledge could remain in `Processing` or `ERROR` status with associated vectors.
  - Reprocessing the knowledge would result in reinserting the vectors into the database, leading to duplicate vectors for the same knowledge.

1. Set the knowledge status to `ERROR`.
2. Continue processing.

| Note: This means that some knowledges will remain in an errored state. Currently, they are not automatically rescheduled for processing.

#### Uncatchable Errors (e.g., worker process fails):

- The task will be automatically retried three times, handled by Celery.
- The notifier will receive an event indicating the task has failed.
- The notifier will set the knowledge status to `ERROR` for the task.

---

🔴 **NOTE: Sync Error Handling for Version v0.1:**

For `process_knowledge` tasks involving the processing of a sync folder, the folder's status will be set to `ERROR`. If child knowledges associated with the sync have already been created, their status cannot be set to `ERROR`. This would leave them stuck in `PROCESSING` status while their parent has an `ERROR` status.

Why can’t we set all children to `ERROR`? This introduces a potential race condition: Sync knowledge can be added to a brain independently from its parent, so it’s unclear if the `PROCESSING` status is tied to the failed task. Although keeping a `task_id` associated with `knowledge_id` could help, it’s error-prone and impacts the database schema, which would have significant consequences.

However, sync knowledge added to a brain will be reprocessed after some time through the sync update task, ensuring that their status will eventually be set to the correct state.

---

## Notification Steps

To discuss: @StanGirard @Zewed
