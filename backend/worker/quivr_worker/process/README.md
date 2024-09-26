# Processing Knowledges

## Processing steps

- Task received a `knowledge_id : UUID`.
- `KnowledgeProcessor.process_knowlege` processes the knowledge:
  - Builds a processable tuple of [Knowledge,QuivrFile] stream:
    - Gets the `KnowledgeDB` object from db:
    - Matches based on the knowledge source:
      - **local**:
        - Downloads the knowledge data from S3 storage and writes it to tempfile
        - Yields the [Knowledge,QuivrFile]
    - **web**: works a lot like **local**...
    - **[syncs]**:
      - Get the associated sync and checks the credentials
      - Concurrently fetches all knowledges for user that are in db associated with this sync and the tree of sync files this knowledge is the parent of (using the sync provider)
      - Downloads knowledge and yields the first [knowledge,QuivrFile]. This is the one this task received
      - For all children of this knowledges (ie: those fetched from the sync):
        - If child in db (ie we have knowledge where `knowledge.sync_id == sync_file.id`):
          - Implies that we could have sync children that were processed before in some other brain
          - if it is PROCESSED Link it to the parent brains and move on
          - ELSE reprocess the file
        - Else:
          - Create the knowledge associated with this sync file and set it to Processing
          - Downloads syncfile data and yield the [knowledge,quivr_file]
  - Skip processing of the tuple if the knowledge is folder
  - Parse the QuivrFile using `quivr-core`
  - Store the chunks in the DB
  - Update knowledge status to PROCESSED

If an exception occurs during the parsing loop we do the following:

### Catchable error:

1. We first the current transaction Rollback (only affects the vectors) if they were set. The processing loop has the following stateful operations in this order:

- Creating knowledges (with processing status)
- Updating knowledges: linking to brains
- Creating vectors
- Updating knowledges

Here is the transaction SAFETY for each operation. These could change and we need to keep the transactional garantees in mind:

- Creation operations and linking to brains can be retried safely. Knowledge is only recreated if they do not exist in DB. Which means we get we can safely retry this operation

- Linking km to brain only link brain if it's not already associated with km. Safe for retry

- Creating vectors :

  - This operation should be rollback if we have an error after. Because we would have a knowledge in Processing/ ERROR status with associated vectors.

  - Reprocessing the knowledge would mean reinserting vectors in the db. This means ending up with duplicate vectors for the same knowledge !

2. Set knowledge to error

3. Continue processing

| This would mean that some knowledges would be errored. For now we don't automatically reschedule them for processing right after.

### Uncatchable error ie worker process fails:

- The task will be automatically retried 3 times -> handled by celery
- Notifier will receive event task as failed
- Notifier sets knowledge status to ERROR for the task

🔴 **NOTE: Sync error handling for the v0.1 version:**

`process_knowledge` tasks that need to process a sync folder, the folder will be set to ERROR.
If we have created child knowledges associated with sync, we can't really set their status to ERROR. This would mean that they will be stuck at status PROCESSING with their parent with an ERROR status.

Why can't we set all children to ERROR? This could introduce a subtle race condition: sync knowledge can be added to brain independently from their parent so we can't know for sure if the status PROCESSING is associated with the task that just failed. We could keep a `task_id` associated with knowledge_id but this is bug prone and impacts the db schema which has a large impact.

The knowledge (syncs) that are added to some brain will be reprocessed after some period of time in the update sync task so their status will be eventually set to the correct state.

## Notification steps

TO discuss @StanGirard @Zewed
