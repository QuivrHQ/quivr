# Processing Knowledges

## Processing steps

- Task received a `knowledge_id : UUID`.
- `KnowledgeProcessor.porcess_knowlege` processes the knowledge:
  - Builds a processable tuple of [Knowledge,QuivrFile] stream:
    - Gets the `KnowledgeDB` object from db:
    - Matches based on the knowledge source:
      - **local**:
        - Downloads the knowledge data from S3 storage and writes it to tempfile
        - Yields the
    - **web**: works a lot like **local**...
    - **syncs**:
      - Get the associated sync and checks the credentials
      - Concurrently fetch all knowledges for user that are in db associated with this sync and the tree of sync files which the knowledge is the parent (using the sync provider)
      - Downloads knowledge and yields the [knowledge,QuivrFile]
      - For all children of this knowledges (those fetched from the sync):
        - If child in db (ie we have knowledge where `knowledge.sync_id == sync_file.id`):
          - Implies that we could have sync children that were processed before in some other brain
          - Link it to the parent brains and move on if it is PROCESSED ELSE Reprocess the file
          - We are done here
        - Else:
          - Create the knowledge associated with this sync file and set it to Processing
          - Downloads syncfile data and yield the [knowledge,quivr_file]

In the processing loop for each processable [KnowledgeDB,Quivrfile], if an exception raised we need to deal with this:

### Catchable error:

1. Rollback (only affects the vectors) if they were set.

- Stateful operations are in order:

  - Creating knowledges (with processing status)
  - Updating knowledges: linking to brains
  - Creating vectors
  - Updating knowledges

- Creation operations and linking to brains can be retried safely. Knowledge is only recreated if they do not exist in DB. Which means we get we can safely retry this operation

- Linking km to brain only link brain if it's not already associated with km. Safe for retry

- Creating vectors :

  - This operation should be rollback if we have an error after. Because we would have a knowledge in Processing/ ERROR status with associated vectors.

  - Reprocessing the knowledge would mean reinserting vectors in the db. which would insert duplicate vectors !

2. Set knowledge to error

3. Continue processing

| This would mean that some knowledges would be errored. For now we don't automatically reprocess the knowledge right after.

### Uncatchable error ie worker process fails:

- The task will be automatically retried 3 times.
- Notifier will receive event task as failed
- Notifier sets knowledge status to ERROR for the task

**NOTE**: for the v0.1 version:
For `process_knowledge` tasks that need to process a sync folder, the folder will be set to ERROR. If we have created child knowledges associated with sync, we can't really set their status to ERROR. This would mean that they are showed as PROCESSING.

## Notification steps

TO discuss @StanGirard @Zewed
