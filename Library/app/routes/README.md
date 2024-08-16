# Exception Handling in CRUD Operations

## Author Routes

### Insert Author (`POST /authors/`)
- **Exceptions Handled**:
  - **Validation Error**: Raised when the request payload is invalid (e.g., missing `name`).
    - **Response**: Returns a 400 status code with an error message.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

### Get Author (`GET /authors/<int:id>`)
- **Exceptions Handled**:
  - **Not Found Error**: Raised when the author with the specified ID does not exist.
    - **Response**: Returns a 404 status code with an error message.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

### Update Author (`PUT /authors/<int:id>`)
- **Exceptions Handled**:
  - **Validation Error**: Raised when the request payload is invalid (e.g., missing `bio`).
    - **Response**: Returns a 400 status code with an error message.
  - **Not Found Error**: Raised when the author with the specified ID does not exist.
    - **Response**: Returns a 404 status code with an error message.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

### Delete Author (`DELETE /authors/<int:id>`)
- **Exceptions Handled**:
  - **Not Found Error**: Raised when the author with the specified ID does not exist.
    - **Response**: Returns a 404 status code with an error message.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

## General Notes
- **Transaction Rollback**: For all general exceptions, the transaction is rolled back using `db.session.rollback()` to ensure no partial changes are saved to the database.
- **Error Responses**: All exceptions return a JSON object with the key `"error"` and a corresponding error message. HTTP status codes are used to indicate the type of error:
  - `400`: Bad Request
  - `404`: Not Found
  - `500`: Internal Server Error

### Recommendations
- **Testing**: Ensure all exception handling paths are thoroughly tested to confirm that the correct responses are returned.
- **Logging**: Consider adding logging for exceptions to help with debugging and monitoring in a production environment.


## Book Routes

### Insert Book (`POST /books/`)
- **Exceptions Handled**:
  - `IntegrityError`: Raised when there is a constraint violation such as a duplicate ISBN.
    - **Response**: Returns a 400 status code with a relevant error message.
  - `Exception`: Any other general errors.
    - **Response**: Returns a 500 status code with the error message.

### Get Book (`GET /books/<int:id>`)
- **Exceptions Handled**:
  - `NoResultFound`: Raised when the book with the given ID does not exist.
    - **Response**: Returns a 404 status code with an error message.
  - `Exception`: Any other general errors.
    - **Response**: Returns a 500 status code with the error message.

### Update Book (`PUT /books/<int:id>`)
- **Exceptions Handled**:
  - `Exception`: Similar handling as in Insert Book.

### Delete Book (`DELETE /books/<int:id>`)
- **Exceptions Handled**:
  - `NoResultFound`: Raised when the book with the given ID does not exist.
    - **Response**: Returns a 404 status code with an error message.
  - `Exception`: Similar handling as in Insert Book.


## BorrowRecord Routes

### Insert Borrow Record (`POST /borrowRecords/`)
- **Exceptions Handled**:
  - **Validation Error**: Raised when the request payload is invalid (e.g., missing required fields like `borrow_date`, `book_id`, or `user_id`).
    - **Response**: Returns a 400 status code with an error message `"Bad request"`.
  - **Date Format Error**: Raised when the date format is incorrect (expected format: `YYYY-MM-DD`).
    - **Response**: Returns a 400 status code with an error message `"Invalid date format. Expected YYYY-MM-DD"`.
  - **IntegrityError**: Raised when a foreign key constraint is violated (e.g., `book_id` or `user_id` does not exist).
    - **Response**: Returns a 404 status code with an error message `"Foreign key constraint error. Check if book_id and user_id exist"`.
  - **DataError**: Raised when there is an issue with the data provided (e.g., data type mismatch).
    - **Response**: Rolls back the transaction and returns a 400 status code with an error message `"Data Error: <original error message>"`.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

### Get Borrow Record (`GET /borrowRecords/<int:id>`)
- **Exceptions Handled**:
  - **Not Found Error**: Raised when the borrow record with the specified ID does not exist.
    - **Response**: Returns a 404 status code with an error message `"This BorrowRecord does not exist"`.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

### Update Borrow Record (`PUT /borrowRecords/<int:id>`)
- **Exceptions Handled**:
  - **Validation Error**: Raised when the request payload is invalid (e.g., missing required fields like `book_id`, `user_id`, or `return_date`).
    - **Response**: Returns a 400 status code with an error message `"Bad request"`.
  - **Date Format Error**: Raised when the date format is incorrect (expected format: `YYYY-MM-DD`).
    - **Response**: Returns a 400 status code with an error message `"Invalid date format. Expected YYYY-MM-DD"`.
  - **IntegrityError**: Raised when a foreign key constraint is violated (e.g., `book_id` or `user_id` does not exist).
    - **Response**: Returns a 400 status code with an error message `"Foreign key constraint error. Check if ids exist"`.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

### Delete Borrow Record (`DELETE /borrowRecords/<int:id>`)
- **Exceptions Handled**:
  - **Not Found Error**: Raised when the borrow record with the specified ID does not exist.
    - **Response**: Returns a 400 status code with an error message `"Bad request"`.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

## Borrow Record Routes

### Create Borrow Record (`POST /borrow_record`)
- **Exceptions Handled**:
  - **Validation Error**: Raised when the request payload is invalid (e.g., missing `borrow_date`, `book_id`, or `user_id`).
    - **Response**: Returns a 400 status code with an error message.
  - **Foreign Key Constraint Error**: Raised when `book_id` or `user_id` references a non-existing record.
    - **Response**: Returns a 404 status code with an error message.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

### Get Borrow Record (`GET /borrow_record/<int:id>`)
- **Exceptions Handled**:
  - **Not Found Error**: Raised when the borrow record with the specified ID does not exist.
    - **Response**: Returns a 404 status code with an error message.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

### Update Borrow Record (`PUT /borrow_record/<int:id>`)
- **Exceptions Handled**:
  - **Validation Error**: Raised when the request payload is invalid (e.g., incorrect `return_date` format).
    - **Response**: Returns a 400 status code with an error message.
  - **Not Found Error**: Raised when the borrow record with the specified ID does not exist.
    - **Response**: Returns a 404 status code with an error message.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

### Delete Borrow Record (`DELETE /borrow_record/<int:id>`)
- **Exceptions Handled**:
  - **Not Found Error**: Raised when the borrow record with the specified ID does not exist.
    - **Response**: Returns a 404 status code with an error message.
  - **Exception**: Any other general errors.
    - **Response**: Rolls back the transaction and returns a 500 status code with the error message.

## General Notes
- **Transaction Rollback**: For all general exceptions, the transaction is rolled back using `db.session.rollback()` to ensure no partial changes are saved to the database.
- **Error Responses**: All exceptions return a JSON object with the key `"error"` and a corresponding error message. HTTP status codes are used to indicate the type of error:
  - `400`: Bad Request
  - `404`: Not Found
  - `500`: Internal Server Error

### Recommendations
- **Testing**: Ensure all exception handling paths are thoroughly tested to confirm that the correct responses are returned.
- **Logging**: Consider adding logging for exceptions to help with debugging and monitoring in a production environment.


## User Details Route

### Get User Details (`GET /user-details`)
- **Description**: 
  - This route returns the details of the authenticated user. To access this route, the user must provide a valid token in the `Authorization` header.
  - The response includes the user's ID, username, role, token, request count, and last request time.

- **Exceptions Handled**:
  - **Authentication Error**: Raised when the user is not authenticated or does not provide a valid token.
    - **Response**: Returns a 401 status code with an error message.
  - **Exception**: Any other general errors encountered while processing the request.
    - **Response**: Returns a 500 status code with an error message.

- **Response Format**:
  - **Success (200)**: A JSON object containing the user's details.
    ```json
    {
      "id": 1,
      "username": "exampleuser",
      "role": "admin",
      "token": "jwt_token_here",
      "request_count": 15,
      "last_request_time": "2024-08-16T12:34:56Z"
    }
    ```
  - **Error (401)**: If the user is not authenticated or token is invalid.
    ```json
    {
      "Error": "Unauthorized access or invalid token."
    }
    ```
  - **Error (500)**: For any other server errors.
    ```json
    {
      "Error": "An internal server error occurred."
    }
    ```

- **Recommendations**:
  - **Token Validation**: Ensure the `protected_routes` decorator correctly validates the token and handles unauthorized access.
  - **Error Handling**: Ensure that error messages are clear and provide sufficient information for debugging.
  - **Testing**: Test the route with valid and invalid tokens to verify that proper responses are returned for different scenarios.
  - **Logging**: Consider logging detailed error messages for debugging and monitoring purposes in a production environment.

