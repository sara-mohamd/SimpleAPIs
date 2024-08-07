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

