# PostgreSQL test owners

Follow [the testing standard](../../../docs/agents/testing.md) before changing these tests.

- Require each expected identity exactly once before checking rows or accepting an empty refusal; missing map keys are not successful admissions.
- Check pinned optional space keys against literal fixture keys before using the job or returned coverage as evidence.
- Retain real SQL, indexed-work, migration and concurrency owners when fake-store or assembled tests cannot reach their failures.
- Journal tracers need a fresh statement-capture witness for committing windows and upper bounds on exchanges; replay may legitimately do zero work. Keep harmless SQL formatting valid.
- Keep private-destination policy proof through Deliverer.Run: Step alone misses Run-specific client initialization.
- Distinguish exports compiled only in _test.go from production seams; remove support only after finding all callers.
