# Backend code guidelines

## **Code Structure and Organization**

- Follow a clear project structure :
    - In quivr-api we have modules divided into : controller, entity, services, repositories, utils)
- **Use dependency injection for better testability and modularity** 🔺
- Use environment variables for configuration 🔺
    - We use Pydantic settings for parsing the arguments
- Don’t add unnecessary abstractions → **KISS principle.**
    - Premature abstractions are a bad pattern
- Avoid using Global Scoped Objects 🔺🔺🔺
- Understand the implications of using the following syntax: 🔺🔺🔺
    - Context manager :
    - Wrapper functions and High order Function
    - Generator / AsyncGenerators
    - ThreadPools and ProcessPool
    - Asynchronous code
- Don’t replicate object that are Standalone/Singleton or with heavy dependencies. All python objects are references. Use the references: 🔺🔺🔺
    - **Example**: Recreating a `BrainService`  inside a function is an antipattern. This function should take `service : BrainService` as a parameter ( also easily testable via dependency injection)
    - **Example**: Recreating a class that connects to a `APIService` is an antipattern. Connection creation is pretty costly process. You should the a **single object** and pass it accross function calls
- Error handling:
    - Use specific exception types rather than catching all exceptions. The caller can then `try .. except CustomException`
    - Create custom exception classes for **application-specific errors.**
    - Add logs when Errors are catched for better debugging

        ```python
        try:
            result = perform_operation()
        except OperationError as e:
            log.error(f"Operation failed: {str(e)}")
            return error_response()
        ```

    - Consider using **assertion statements ! IMHO this is really important** 🔺. Checkout : https://github.com/tigerbeetle/tigerbeetle/blob/main/docs/TIGER_STYLE.md#safety

**(Advanced):**

- Try encoding business pattern in Type ( known as Typestate pattern):
    - For example if a File can either be in Open or Close state → use two Types OpenFile and CloseFile with separate behaviour to avoid calling methods on a closed file.
- May need to consider adding route level exception handling to FastAPI

## **Database and ORM**

- Use SQLModel for all database operations:
    - SQlmodel docs : [https://sqlmodel.tiangolo.com/](https://sqlmodel.tiangolo.com/)
    - Use **eager** or **lazy** relationship for modeling 1-many and many-many relationships depending on join cost
    - Be aware of async session and lazy attributes
- Use async as much as possible
- Think about access patterns in your code :  🔺🔺🔺
    - Reduce n+1 calls : If we can get the information with a single query, we do it in a single query

    > **Always ask if this chunk of call can be done via a single SQL query !**
    >
    - Batch writes to the database. If we Insert N times in a loop → 1 insert many !
    - Write database queries with proper indexing in mind.
        - Example : Do we need to filter results ? If yes then add a WHERE clause …
        - Do we frequently filter on some attribute → Add index.
        - Think about which index :BTreeIndex when ordered access, HashIndex where data is really dissimilar and we need extremely fast access …
    - Think about Joins. If we do 2 queries to get the data then maybe we can do it in one :
        - For example User/UserSettings/UserUsage. We can get all of this info eagerly when accessing user.

            > DB side fetching is FAST ! Network is slow !
            >
- Think about atomic guarantees and transactions in the whole workflow
    - Example : deleting a knowledge and its vectors should be atomic

## **API and External Services**

- When sending requests to external services (APIs), always include:
    - Defined timeouts
    - Backoff policy
    - Retry mechanism
    - Conversion of HTTP errors to business-level exceptions
- Use a circuit breaker pattern for frequently called external services
- Implement proper **error handling and logging**

## **HTTP and Routing**

- Keep HTTP logic confined to the routes layer
- Raise HTTP errors only through FastAPI
- Use appropriate HTTP status codes consistently with
- Implement request validation at the API entry point

## **Performance**

- Use caching mechanisms where appropriate (e.g., Redis)
- Implement pagination for list endpoints
- Use asynchronous programming where beneficial
    - Keep in mind that python is single threaded !
- Avoid unnecessary serialization/deserialization
- Optimize database queries and use indexing effectively
- For performance critical code :
    - Use libraries that are True wrappers (ie don’t call subprocess)
    - Use libraries that  release the GIL
    - Use Threadpools and ProcessPool when possible
    - Be aware of libraries spawning their own threadpool !!!!
- Understand underlying systems : networks, disk access, operating system syscalls

## **Testing**

- Write unit tests for all business logic. The code should be written with dependency injection in mind !
- Write unit test for repositories:
    - Use the rollback session fixture ( see ChatHistory tests)
    - Test with different configurations of Brain types, User settings, … → Use parametrized test for this
- Implement integration tests for API endpoints
    - FastAPI testclient :  https://fastapi.tiangolo.com/tutorial/testing/
- Use mocking for external services in tests.

## **Logging and Monitoring**

- Implement structured logging
- *TODO: define where and how*

## **Security**

- Implement input validation and sanitization
- Use parameterized queries to prevent SQL injection
- Implement rate limiting for API endpoints
- Regularly update dependencies and address security vulnerabilities

## **Documentation**

- Maintain a README with setup and run instructions
- Document all non-obvious code sections

## **Version Control and CI/CD**

- Use feature branches and pull requests
- Keep a changelog for version control
- Implement automated CI/CD pipelines
- **Perform code reviews for all changes**
